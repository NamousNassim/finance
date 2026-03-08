from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
import calendar

try:
    from dateutil.relativedelta import relativedelta
except ImportError:  # lightweight fallback
    relativedelta = None

from django.db import transaction
from django.utils import timezone

from .models import (
    Facture, LigneFacture,
    FactureStatut, FactureType, RecurrenceFrequence,
)


def quantize(value: Decimal) -> Decimal:
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def compute_invoice_totals(facture):
    """
    Recalcule les totaux d'une facture à partir de ses lignes.
    Met à jour subtotal_ht, tva_amount et total_ttc en mémoire.
    """
    subtotal = sum((l.total_ht for l in facture.lignes.all()), Decimal('0.00'))
    tva = quantize(subtotal * (facture.tva_rate / Decimal('100')))
    total = quantize(subtotal + tva)
    facture.subtotal_ht = quantize(subtotal)
    facture.montant_ht = facture.subtotal_ht
    facture.tva_amount = tva
    facture.total_ttc = total
    return facture


# ——— Récurrence ———

def _add_months(base_date: date, months: int) -> date:
    """Ajoute des mois en conservant le dernier jour si nécessaire (fallback sans dateutil)."""
    month = base_date.month - 1 + months
    year = base_date.year + month // 12
    month = month % 12 + 1
    day = min(base_date.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def calculate_next_generation_date(start_date: date, frequence: str) -> date:
    """
    Calcule la prochaine date à partir de la date de départ et de la fréquence.
    """
    if start_date is None:
        return None

    if relativedelta:
        if frequence == RecurrenceFrequence.MENSUELLE:
            return start_date + relativedelta(months=+1)
        if frequence == RecurrenceFrequence.TRIMESTRIELLE:
            return start_date + relativedelta(months=+3)
        if frequence == RecurrenceFrequence.ANNUELLE:
            return start_date + relativedelta(years=+1)
    else:
        if frequence == RecurrenceFrequence.MENSUELLE:
            return _add_months(start_date, 1)
        if frequence == RecurrenceFrequence.TRIMESTRIELLE:
            return _add_months(start_date, 3)
        if frequence == RecurrenceFrequence.ANNUELLE:
            return _add_months(start_date, 12)

    return start_date


@transaction.atomic
def generate_invoice_from_template(template: Facture, generation_date: date | None = None) -> Facture:
    """
    Génère une facture ponctuelle à partir d'un modèle récurrent.
    Copie les lignes et recalcule les totaux.
    """
    if not template.is_recurring_template():
        raise ValueError("La facture source doit être un modèle récurrent.")
    if not template.recurrence_active:
        raise ValueError("La récurrence est désactivée pour ce modèle.")
    if not template.recurrence_prochaine:
        raise ValueError("Aucune date de prochaine génération définie.")

    generation_date = generation_date or template.recurrence_prochaine or timezone.now().date()

    # Calcule l'échéance relative si le modèle en possède une
    echeance = None
    if template.date_echeance:
        delta_days = (template.date_echeance - template.date_emission).days
        echeance = generation_date + timedelta(days=delta_days)

    facture = Facture.objects.create(
        client=template.client,
        objet=template.objet,
        montant_ht=Decimal('0.00'),
        subtotal_ht=Decimal('0.00'),
        tva_rate=template.tva_rate,
        tva_amount=Decimal('0.00'),
        total_ttc=Decimal('0.00'),
        statut=FactureStatut.BROUILLON,
        date_emission=generation_date,
        date_echeance=echeance,
        notes=template.notes,
        type_facture=FactureType.PONCTUELLE,
        recurrence_active=False,
        source_recurring=template,
        created_by=template.created_by,
    )

    lignes = [
        LigneFacture(
            facture=facture,
            description=lf.description,
            quantite=lf.quantite,
            prix_unitaire=lf.prix_unitaire,
            item_type=lf.item_type,
        )
        for lf in template.lignes.all()
    ]
    LigneFacture.objects.bulk_create(lignes)

    facture.recompute_totals(save=True)
    return facture


def update_next_generation(template: Facture) -> None:
    """
    Calcule et persiste la prochaine date de génération.
    Désactive la récurrence si la fin est dépassée.
    """
    if not template.recurrence_prochaine or not template.recurrence_frequence:
        template.recurrence_active = False
        template.recurrence_prochaine = None
        template.save(update_fields=['recurrence_active', 'recurrence_prochaine', 'updated_at'])
        return

    new_date = calculate_next_generation_date(template.recurrence_prochaine, template.recurrence_frequence)

    # Si une fin est définie et déjà dépassée par la prochaine date
    if template.recurrence_fin and new_date > template.recurrence_fin:
        template.recurrence_active = False
        template.recurrence_prochaine = None
    else:
        template.recurrence_prochaine = new_date

    template.save(update_fields=['recurrence_active', 'recurrence_prochaine', 'updated_at'])

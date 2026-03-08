from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone

from dashboard.models import Facture, FactureType
from dashboard.services import generate_invoice_from_template, update_next_generation


class Command(BaseCommand):
    help = "Génère les factures issues des modèles récurrents arrivés à échéance."

    def handle(self, *args, **options):
        today = timezone.now().date()
        templates = Facture.objects.filter(
            type_facture=FactureType.RECURRENTE,
            recurrence_active=True,
            recurrence_prochaine__isnull=False,
            recurrence_prochaine__lte=today,
        ).filter(
            models.Q(recurrence_fin__isnull=True) |
            models.Q(recurrence_prochaine__lte=models.F('recurrence_fin'))
        )

        generated = 0
        for template in templates:
            try:
                facture = generate_invoice_from_template(template, generation_date=template.recurrence_prochaine)
                update_next_generation(template)
                generated += 1
                self.stdout.write(self.style.SUCCESS(f"{facture.numero} générée depuis {template.numero}"))
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f"Échec pour {template.numero}: {exc}"))

        self.stdout.write(self.style.NOTICE(f"{generated} facture(s) générée(s)."))

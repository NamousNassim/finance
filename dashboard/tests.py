from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from .models import Client, Facture, FactureStatut, FactureType, LigneFacture, RecurrenceFrequence
from .services import generate_invoice_from_template


class FactureHorsTaxeTests(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(nom="Client TVA")

    def test_recompute_totals_excludes_hors_taxe_lines_from_tva(self):
        facture = Facture.objects.create(
            client=self.client_obj,
            objet="Test TVA selective",
            tva_rate=Decimal("20.00"),
            statut=FactureStatut.BROUILLON,
        )
        LigneFacture.objects.create(
            facture=facture,
            description="Prestation taxable",
            quantite=Decimal("1.00"),
            prix_unitaire=Decimal("100.00"),
            hors_taxe=False,
        )
        LigneFacture.objects.create(
            facture=facture,
            description="Debours hors taxe",
            quantite=Decimal("1.00"),
            prix_unitaire=Decimal("50.00"),
            hors_taxe=True,
        )

        facture.recompute_totals(save=True)
        facture.refresh_from_db()

        self.assertEqual(facture.subtotal_ht, Decimal("150.00"))
        self.assertEqual(facture.tva_amount, Decimal("20.00"))
        self.assertEqual(facture.total_ttc, Decimal("170.00"))

    def test_generate_invoice_from_template_preserves_hors_taxe_flag(self):
        template = Facture.objects.create(
            client=self.client_obj,
            objet="Modele recurrent",
            tva_rate=Decimal("20.00"),
            statut=FactureStatut.BROUILLON,
            type_facture=FactureType.RECURRENTE,
            recurrence_frequence=RecurrenceFrequence.MENSUELLE,
            recurrence_debut=timezone.now().date(),
            recurrence_prochaine=timezone.now().date(),
            recurrence_active=True,
        )
        LigneFacture.objects.create(
            facture=template,
            description="Ligne hors taxe",
            quantite=Decimal("2.00"),
            prix_unitaire=Decimal("75.00"),
            hors_taxe=True,
        )

        generated = generate_invoice_from_template(template)

        self.assertEqual(generated.lignes.count(), 1)
        self.assertTrue(generated.lignes.first().hors_taxe)

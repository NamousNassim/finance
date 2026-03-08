from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_rename_taux_tva_facture_tva_rate_facture_subtotal_ht_and_more'),
    ]

    def set_recurrence_defaults(apps, schema_editor):
        Facture = apps.get_model('dashboard', 'Facture')
        Facture.objects.update(recurrence_active=False)

    operations = [
        migrations.AddField(
            model_name='facture',
            name='recurrence_active',
            field=models.BooleanField(default=True, verbose_name='Récurrence active'),
        ),
        migrations.AddField(
            model_name='facture',
            name='recurrence_debut',
            field=models.DateField(blank=True, null=True, verbose_name='Date de début de récurrence'),
        ),
        migrations.AddField(
            model_name='facture',
            name='recurrence_fin',
            field=models.DateField(blank=True, null=True, verbose_name='Date de fin de récurrence'),
        ),
        migrations.AddField(
            model_name='facture',
            name='recurrence_frequence',
            field=models.CharField(blank=True, choices=[('MENSUELLE', 'Mensuelle'), ('TRIMESTRIELLE', 'Trimestrielle'), ('ANNUELLE', 'Annuelle')], max_length=20, null=True, verbose_name='Fréquence de récurrence'),
        ),
        migrations.AddField(
            model_name='facture',
            name='recurrence_prochaine',
            field=models.DateField(blank=True, null=True, verbose_name='Prochaine génération'),
        ),
        migrations.AddField(
            model_name='facture',
            name='source_recurring',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factures_generees', to='dashboard.facture', verbose_name='Facture source récurrente'),
        ),
        migrations.AddField(
            model_name='facture',
            name='type_facture',
            field=models.CharField(choices=[('PONCTUELLE', 'Facture ponctuelle'), ('RECURRENTE', 'Facture récurrente (modèle)')], default='PONCTUELLE', max_length=20, verbose_name='Type de facture'),
        ),
        migrations.RunPython(set_recurrence_defaults, migrations.RunPython.noop),
    ]

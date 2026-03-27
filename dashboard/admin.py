from django.contrib import admin
from .models import Client, Prospect, Facture, LigneFacture


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'prenom', 'societe', 'email', 'telephone', 'ice', 'statut', 'created_at']
    list_filter   = ['statut', 'created_at']
    search_fields = ['nom', 'prenom', 'email', 'societe', 'siret', 'ice']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Identite', {'fields': ('nom', 'prenom', 'societe', 'siret', 'ice')}),
        ('Contact',  {'fields': ('email', 'telephone', 'adresse')}),
        ('Gestion',  {'fields': ('statut', 'notes', 'created_by')}),
        ('Dates',    {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display  = ['nom', 'prenom', 'societe', 'email', 'statut', 'source',
                     'date_dernier_contact', 'created_at']
    list_filter   = ['statut', 'source', 'created_at']
    search_fields = ['nom', 'prenom', 'email', 'societe']
    readonly_fields = ['created_at', 'updated_at']


class LigneFactureInline(admin.TabularInline):
    model  = LigneFacture
    extra  = 1
    fields = ['description', 'quantite', 'prix_unitaire', 'hors_taxe', 'item_type']


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display    = ['numero', 'client', 'objet', 'subtotal_ht', 'tva_amount', 'total_ttc',
                       'statut', 'type_facture', 'recurrence_active', 'recurrence_prochaine', 'date_emission']
    list_filter     = ['statut', 'type_facture', 'recurrence_active', 'recurrence_frequence', 'date_emission']
    search_fields   = ['numero', 'objet', 'client__nom', 'client__societe']
    readonly_fields = ['numero', 'created_at', 'updated_at', 'subtotal_ht', 'tva_amount', 'total_ttc']
    inlines         = [LigneFactureInline]

    fieldsets = (
        ('Informations', {
            'fields': ('numero', 'client', 'objet', 'notes', 'statut')
        }),
        ('Montants', {
            'fields': (('montant_ht', 'tva_rate'), ('subtotal_ht', 'tva_amount', 'total_ttc'))
        }),
        ('Dates', {
            'fields': ('date_emission', 'date_echeance', 'created_at', 'updated_at')
        }),
        ('Recurrence', {
            'fields': (
                'type_facture', 'recurrence_frequence', 'recurrence_debut',
                'recurrence_fin', 'recurrence_prochaine', 'recurrence_active',
                'source_recurring',
            ),
            'classes': ('collapse',),
        }),
        ('Audit', {
            'fields': ('created_by',),
        }),
    )

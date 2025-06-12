# apartamentos/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Comodidade, Predio, Apartamento, FotoApartamento, Perfil

@admin.register(Comodidade)
class ComodidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# ... (O PredioAdmin e os Inlines que já fizemos estão corretos) ...
class ApartamentoInline(admin.TabularInline):
    model = Apartamento
    extra = 1
    fields = ('titulo', 'proprietario', 'numero_quartos', 'preco_diaria', 'disponivel')
    show_change_link = True

class FotoApartamentoInline(admin.TabularInline):
    model = FotoApartamento
    extra = 1
    readonly_fields = ('data_upload',)

@admin.register(Predio)
class PredioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'estado', 'data_cadastro')
    list_filter = ('cidade', 'estado')
    search_fields = ('nome', 'endereco_completo', 'cidade', 'cep')
    inlines = [ApartamentoInline]

# --- CLASSE CORRIGIDA ABAIXO ---
@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    # ATUALIZADO: Removemos 'cidade' e 'estado' daqui
    list_display = ('titulo', 'predio', 'proprietario', 'preco_diaria', 'disponivel')

    # ATUALIZADO: Usamos 'predio__cidade' e 'predio__estado' para filtrar
    list_filter = ('disponivel', 'predio__cidade', 'predio__estado', 'proprietario')

    # ATUALIZADO: Usamos 'predio__nome' para busca
    search_fields = ('titulo', 'predio__nome', 'proprietario__username')

    # O autocomplete_fields já deve estar correto se você copiou da última vez
    autocomplete_fields = ['predio', 'proprietario']
    filter_horizontal = ('comodidades',)
    inlines = [FotoApartamentoInline]

    # O fieldsets também deve estar correto, pois ele já não continha os campos de endereço
    fieldsets = (
        ('Informações da Unidade', {
            'fields': ('predio', 'proprietario', 'titulo', 'descricao')
        }),
        ('Detalhes do Imóvel', {
            'fields': (
                'numero_quartos',
                'numero_banheiros',
                'area_m2',
                'foto_principal'
            )
        }),
        ('Comodidades', {'fields': ('comodidades',)}),
        ('Disponibilidade e Preço', {'fields': ('disponivel', 'preco_diaria')}),
    )

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil do Usuário'
    fk_name = 'usuario'

# Define uma nova classe UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

# Re-registra o admin de User com a nossa versão customizada
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
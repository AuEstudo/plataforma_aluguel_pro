from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Comodidade, Predio, Apartamento, FotoApartamento, Perfil, Reserva

class PerfilInline(admin.StackedInline):
    model = Perfil; can_delete = False; verbose_name_plural = 'Perfil do Usuário'; fk_name = 'usuario'

class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Comodidade)
class ComodidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',); search_fields = ('nome',)

class ApartamentoInline(admin.TabularInline):
    model = Apartamento; extra = 1; fields = ('titulo', 'proprietario', 'numero_quartos', 'preco_diaria', 'disponivel'); show_change_link = True

@admin.register(Predio)
class PredioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'proprietario', 'cidade', 'estado'); list_filter = ('cidade', 'estado', 'proprietario'); search_fields = ('nome', 'proprietario__username'); inlines = [ApartamentoInline]

class FotoApartamentoInline(admin.TabularInline):
    model = FotoApartamento; extra = 1

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'predio', 'proprietario', 'preco_diaria', 'disponivel'); list_filter = ('disponivel', 'predio__cidade', 'proprietario'); search_fields = ('titulo', 'predio__nome'); autocomplete_fields = ['predio', 'proprietario']; filter_horizontal = ('comodidades',); inlines = [FotoApartamentoInline]

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('apartamento', 'hospede', 'data_checkin', 'data_checkout', 'status'); list_filter = ('status', 'data_checkin'); search_fields = ('apartamento__titulo', 'hospede__username'); autocomplete_fields = ['apartamento', 'hospede']
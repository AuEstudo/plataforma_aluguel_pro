from django.urls import path
from .views import (
    ApartamentoListView, ApartamentoDetailView, PredioListView, PredioDetailView,
    SignUpView, perfil_view, PainelProprietarioView, MinhasReservasListView,
    PredioCreateView, ApartamentoCreateView, ApartamentoUpdateView, ApartamentoDeleteView,
    aprovar_reserva, recusar_reserva, ReservaDetailView, reserva_calendario_data
)

app_name = 'apartamentos'

urlpatterns = [
    path('', ApartamentoListView.as_view(), name='lista_apartamentos'),
    path('predios/', PredioListView.as_view(), name='lista_predios'),
    path('predios/<int:pk>/', PredioDetailView.as_view(), name='detalhe_predio'),
    path('apartamento/<int:pk>/', ApartamentoDetailView.as_view(), name='detalhe_apartamento'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('meu-perfil/', perfil_view, name='perfil_edit'),

    path('painel/', PainelProprietarioView.as_view(), name='painel_proprietario'),
    path('minhas-reservas/', MinhasReservasListView.as_view(), name='minhas_reservas'),

    path('predio/novo/', PredioCreateView.as_view(), name='criar_predio'),
    path('predio/<int:pk_predio>/apartamento/novo/', ApartamentoCreateView.as_view(), name='criar_apartamento'),
    path('apartamento/<int:pk>/editar/', ApartamentoUpdateView.as_view(), name='apartamento_update'),
    path('apartamento/<int:pk>/deletar/', ApartamentoDeleteView.as_view(), name='apartamento_delete'),

    path('reserva/<int:pk>/aprovar/', aprovar_reserva, name='aprovar_reserva'),
    path('reserva/<int:pk>/recusar/', recusar_reserva, name='recusar_reserva'),
    path('reserva/<int:pk>/', ReservaDetailView.as_view(), name='detalhe_reserva'),

    path('apartamento/<int:pk_apartamento>/calendario-data/', reserva_calendario_data, name='reserva_calendario_data'),

    path('apartamento/<int:pk>/editar/', ApartamentoUpdateView.as_view(), name='editar_apartamento'),
]

# apartamentos/urls.py
from django.urls import path
from .views import (
    ApartamentoListView,
    ApartamentoDetailView,
    PredioListView,
    PredioDetailView,
    SignUpView,
    perfil_view,
    MeusAnunciosListView,
    PredioCreateView,
    ApartamentoCreateView,
    ApartamentoUpdateView,
    ApartamentoDeleteView
)

app_name = 'apartamentos'

urlpatterns = [
    # URLs de Prédios
    path('predios/', PredioListView.as_view(), name='lista_predios'),
    path('predios/<int:pk>/', PredioDetailView.as_view(), name='detalhe_predio'),
    path('meus-anuncios/', MeusAnunciosListView.as_view(), name='meus_anuncios'),
    path('predio/novo/', PredioCreateView.as_view(), name='predio_create'),
    path('predio/<int:pk_predio>/apartamento/novo/', ApartamentoCreateView.as_view(), name='apartamento_create'),
    path('apartamento/<int:pk>/editar/', ApartamentoUpdateView.as_view(), name='apartamento_update'),
    path('apartamento/<int:pk>/deletar/', ApartamentoDeleteView.as_view(), name='apartamento_delete'),
    path('', ApartamentoListView.as_view(), name='lista_apartamentos'),
    path('<int:pk>/', ApartamentoDetailView.as_view(), name='detalhe_apartamento'),
    path('signup', SignUpView.as_view(), name='signup'),
    # URL de Perfil - vamos ter uma para ver e outra para editar
    # Vamos manter a antiga por enquanto, mas apontando para uma nova view de detalhe se necessário,
    # ou podemos simplesmente ter uma única página de edição como "página de perfil".
    # Vamos simplificar e ter a página /meu-perfil/ como a página de EDIÇÃO.
    path('meu-perfil/', perfil_view, name='perfil_edit'),
    path('meu-perfil/', perfil_view, name='perfil'),

]

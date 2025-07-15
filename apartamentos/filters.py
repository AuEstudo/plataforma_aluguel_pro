import django_filters
from django.forms import TextInput
from .models import Apartamento

class ApartamentoFilter(django_filters.FilterSet):
    # Filtro para a cidade. 'predio__cidade' acessa o campo através da relação.
    # 'lookup_expr='icontains'' faz a busca ser "contém" e case-insensitive.
    predio__cidade = django_filters.CharFilter(
        lookup_expr='icontains',
        label="", # Label vazio para customizarmos no HTML
        widget=TextInput(attrs={'placeholder': 'Qual cidade?', 'class': 'form-control', 'list': 'lista-cidades'})
    )

    class Meta:
        model = Apartamento
        # Aqui definimos os campos do modelo que queremos filtrar.
        # No momento, só precisamos do filtro customizado de cidade.
        # Outros filtros (como preço, quartos) poderiam ser adicionados aqui.
        fields = []
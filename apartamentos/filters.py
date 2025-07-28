# apartamentos/filters.py
import django_filters
from django.forms import TextInput
from .models import Apartamento

class ApartamentoFilter(django_filters.FilterSet):
    predio__cidade = django_filters.CharFilter(
        lookup_expr='icontains',
        label="",
        widget=TextInput(attrs={
            'placeholder': 'Qual cidade?',
            'class': 'form-control',
            'list': 'lista-cidades'
        })
    )

    class Meta:
        model = Apartamento
        fields = [] # Apenas o filtro de cidade, definido acima, será usado.
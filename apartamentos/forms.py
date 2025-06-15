# apartamentos/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Predio, Apartamento, Perfil

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')


class PredioForm(forms.ModelForm):
    class Meta:
        model = Predio
        # Listamos os campos que o usuário poderá preencher.
        # O 'proprietario' será definido automaticamente pela view.
        fields = ['nome', 'endereco_completo', 'cidade', 'estado', 'cep', 'foto_fachada']
        # Opcional: Adicionar widgets para estilização com Bootstrap
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_fachada': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Formulário para criar e editar Apartamentos
class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        # O 'proprietario' e o 'predio' serão definidos pela view.
        fields = [
            'titulo', 'descricao', 'numero_quartos', 'numero_banheiros',
            'area_m2', 'preco_diaria', 'foto_principal', 'disponivel', 'comodidades'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'numero_quartos': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_banheiros': forms.NumberInput(attrs={'class': 'form-control'}),
            'area_m2': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_diaria': forms.NumberInput(attrs={'class': 'form-control'}),
            'foto_principal': forms.FileInput(attrs={'class': 'form-control'}),
            'disponivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comodidades': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
        }

# Formulário para editar dados do User (nome, email)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {  # Adicionando classes para estilização
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# Formulário para editar dados do Perfil (foto, telefone, bio)
class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil', 'telefone', 'bio']
        widgets = {
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
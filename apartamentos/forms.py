from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Predio, Apartamento, Perfil, Reserva, Avaliacao


class CustomUserCreationForm(UserCreationForm):
    papel = forms.ChoiceField(
        choices=[
            ('CLIENTE', 'Quero alugar (Cliente)'),
            ('PROPRIETARIO', 'Quero anunciar (Proprietário)'),
        ],
        widget=forms.RadioSelect,
        required=True,
        label="Qual seu objetivo na plataforma?"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}), 'last_name': forms.TextInput(attrs={'class': 'form-control'}), 'email': forms.EmailInput(attrs={'class': 'form-control'})}

class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil', 'telefone', 'bio']
        widgets = {'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}), 'telefone': forms.TextInput(attrs={'class': 'form-control'}), 'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})}

class PredioForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = ['nome', 'endereco_completo', 'cidade', 'estado', 'cep', 'foto_fachada']
        widgets = {'nome': forms.TextInput(attrs={'class': 'form-control'}), 'endereco_completo': forms.TextInput(attrs={'class': 'form-control'}), 'cidade': forms.TextInput(attrs={'class': 'form-control'}), 'estado': forms.TextInput(attrs={'class': 'form-control'}), 'cep': forms.TextInput(attrs={'class': 'form-control'}), 'foto_fachada': forms.FileInput(attrs={'class': 'form-control'})}

class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = ['titulo', 'descricao', 'numero_quartos', 'numero_banheiros', 'area_m2', 'preco_diaria', 'foto_principal', 'disponivel', 'comodidades']
        widgets = {'titulo': forms.TextInput(attrs={'class': 'form-control'}), 'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), 'numero_quartos': forms.NumberInput(attrs={'class': 'form-control'}), 'numero_banheiros': forms.NumberInput(attrs={'class': 'form-control'}), 'area_m2': forms.NumberInput(attrs={'class': 'form-control'}), 'preco_diaria': forms.NumberInput(attrs={'class': 'form-control'}), 'foto_principal': forms.FileInput(attrs={'class': 'form-control'}), 'disponivel': forms.CheckboxInput(attrs={'class': 'form-check-input'}), 'comodidades': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5})}

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data_checkin', 'data_checkout']
        widgets = {
            'data_checkin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_checkout': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.apartamento = kwargs.pop('apartamento', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        data_checkin = cleaned_data.get("data_checkin")
        data_checkout = cleaned_data.get("data_checkout")

        if not data_checkin or not data_checkout:
            return cleaned_data

        if data_checkin < timezone.localdate():
            self.add_error('data_checkin', "Não é possível iniciar uma reserva em uma data no passado.")
            return cleaned_data

        if data_checkin >= data_checkout:
            self.add_error('data_checkout', "A data de Check-out deve ser, no mínimo, o dia seguinte ao Check-in.")
            return cleaned_data

        if self.apartamento:
            status_bloqueantes = [Reserva.StatusReserva.CONFIRMADA, Reserva.StatusReserva.PENDENTE]

            # --- LÓGICA MATEMÁTICA CORRETA E DEFINITIVA ---
            # Verifica se o início de uma reserva é antes ou no mesmo dia do fim da outra,
            # e vice-versa. Isso cobre todos os casos de sobreposição e de "toque".
            reservas_conflitantes = Reserva.objects.filter(
                apartamento=self.apartamento,
                status__in=status_bloqueantes,
                data_checkin__lte=data_checkout,  # Início da reserva existente <= Fim da nova
                data_checkout__gte=data_checkin  # Fim da reserva existente >= Início da nova
            )

            if self.instance and self.instance.pk:
                reservas_conflitantes = reservas_conflitantes.exclude(pk=self.instance.pk)

            if reservas_conflitantes.exists():
                raise ValidationError(
                    "Conflito de datas! O período selecionado (ou parte dele) já está ocupado.",
                    code='conflito_reserva'
                )

        return cleaned_data

class ApartamentoSearchForm(forms.Form):
    cidade = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Qual cidade?'}))
    data_checkin = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    data_checkout = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))


class AvaliacaoForm(forms.ModelForm):
    nota = forms.ChoiceField(
        choices=[(i, f'{i} Estrela{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )

    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
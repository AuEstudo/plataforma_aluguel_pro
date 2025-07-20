import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Predio, Apartamento, Reserva, Avaliacao

# ... (imports) ...

# --- NOSSA PRIMEIRA FIXTURE ---
@pytest.fixture
def cenario_reserva():
    """
    Cria um cenário base com proprietário, hóspede, prédio e apartamento
    para ser reutilizado nos testes de reserva.
    """
    proprietario = User.objects.create_user(username='proprietario_teste_reserva')
    hospede = User.objects.create_user(username='hospede_teste_reserva')
    predio = Predio.objects.create(nome='Prédio para Reservas', proprietario=proprietario)
    apartamento = Apartamento.objects.create(
        titulo='Apto para Reservas',
        predio=predio,
        proprietario=proprietario,
        area_m2=50.00,
        preco_diaria=200.00
    )
    return {'apartamento': apartamento, 'hospede': hospede}

# ... (testes existentes) ...

@pytest.mark.django_db
def test_avaliacao_str_representation():
    """
    Teste unitário para verificar a representação em string do modelo Avaliacao.
    """
    # 1. Arrange (Organizar): Criamos todos os objetos necessários.
    proprietario = User.objects.create_user(username='proprietario_teste')
    hospede = User.objects.create_user(username='hospede_teste')

    predio = Predio.objects.create(nome='Prédio de Teste', proprietario=proprietario)

    # --- CORREÇÃO AQUI ---
    # Adicionamos os campos obrigatórios 'area_m2' e 'preco_diaria'.
    apartamento = Apartamento.objects.create(
        titulo='Apartamento de Teste',
        predio=predio,
        proprietario=proprietario,
        area_m2=50.00,
        preco_diaria=150.00
    )

    reserva = Reserva.objects.create(
        apartamento=apartamento,
        hospede=hospede,
        data_checkin='2025-01-01',
        data_checkout='2025-01-05'
    )
    avaliacao = Avaliacao.objects.create(reserva=reserva, nota=5, comentario="Ótimo!")

    # 2. Act (Agir)
    representacao_str = str(avaliacao)

    # 3. Assert (Verificar)
    assert representacao_str == 'Avaliação de hospede_teste para Apartamento de Teste'


@pytest.mark.django_db
def test_homepage_loads_successfully(client):
    """
    Teste de integração para verificar se a Homepage carrega.
    """
    url = reverse('homepage')
    response = client.get(url)
    assert response.status_code == 200

# Adicione a importação do formulário que vamos testar
from .forms import ReservaForm

# ... (fixtures e testes existentes) ...

@pytest.mark.django_db
def test_reserva_form_valido(cenario_reserva):
    """
    Verifica se o ReservaForm é considerado válido com datas corretas.
    """
    # Arrange: Preparamos os dados para o formulário.
    dados_validos = {
        'data_checkin': '2025-08-01',
        'data_checkout': '2025-08-05'
    }
    # Passamos o apartamento da fixture para o formulário, como nossa view faz.
    form = ReservaForm(data=dados_validos, apartamento=cenario_reserva['apartamento'])

    # Act & Assert: Verificamos se o formulário é válido.
    assert form.is_valid()

# ...

@pytest.mark.django_db
def test_reserva_form_data_passada_invalido(cenario_reserva):
    """
    Verifica se o formulário invalida uma tentativa de reserva no passado.
    """
    # Arrange: Datas no passado.
    dados_invalidos = {
        'data_checkin': '2020-01-01',
        'data_checkout': '2020-01-05'
    }
    form = ReservaForm(data=dados_invalidos, apartamento=cenario_reserva['apartamento'])

    # Act & Assert: Verificamos que o formulário NÃO é válido.
    assert not form.is_valid()
    # E que o erro está associado ao campo 'data_checkin'.
    assert 'data_checkin' in form.errors


@pytest.mark.django_db
def test_reserva_form_conflito_de_datas_invalido(cenario_reserva):
    """
    Verifica se o formulário invalida uma reserva que conflita com uma existente.
    """
    # Arrange: Primeiro, criamos uma reserva que já existe no banco de dados.
    Reserva.objects.create(
        apartamento=cenario_reserva['apartamento'],
        hospede=cenario_reserva['hospede'],
        data_checkin='2025-09-10',
        data_checkout='2025-09-15'
    )
    # Agora, tentamos criar uma nova reserva que se sobrepõe à existente.
    dados_conflitantes = {
        'data_checkin': '2025-09-12',
        'data_checkout': '2025-09-17'
    }
    form = ReservaForm(data=dados_conflitantes, apartamento=cenario_reserva['apartamento'])

    # Act & Assert: Verificamos que o formulário NÃO é válido.
    assert not form.is_valid()
    # E que o erro é um erro geral do formulário (não associado a um campo específico).
    assert '__all__' in form.errors
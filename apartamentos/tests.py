import pytest
from django.contrib.auth.models import User
from django.urls import reverse

# Modelos e Forms que já estávamos usando
from .models import Predio, Apartamento, Reserva, Avaliacao
from .forms import ReservaForm

# --- AQUI ESTÁ A LINHA QUE FALTAVA ---
# Importamos as funções de serviço que queremos testar.
from .services import aprovar_reserva_service, recusar_reserva_service


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
    return {'apartamento': apartamento, 'hospede': hospede, 'proprietario': proprietario}


@pytest.mark.django_db
def test_avaliacao_str_representation():
    # ... (este teste continua igual) ...
    proprietario = User.objects.create_user(username='proprietario_teste')
    hospede = User.objects.create_user(username='hospede_teste')
    predio = Predio.objects.create(nome='Prédio de Teste', proprietario=proprietario)
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
    representacao_str = str(avaliacao)
    assert representacao_str == 'Avaliação de hospede_teste para Apartamento de Teste'


@pytest.mark.django_db
def test_homepage_loads_successfully(client):
    # ... (este teste continua igual) ...
    url = reverse('homepage')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_reserva_form_valido(cenario_reserva):
    # ... (este teste continua igual) ...
    dados_validos = {'data_checkin': '2025-08-01', 'data_checkout': '2025-08-05'}
    form = ReservaForm(data=dados_validos, apartamento=cenario_reserva['apartamento'])
    assert form.is_valid()


@pytest.mark.django_db
def test_reserva_form_data_passada_invalido(cenario_reserva):
    # ... (este teste continua igual) ...
    dados_invalidos = {'data_checkin': '2020-01-01', 'data_checkout': '2020-01-05'}
    form = ReservaForm(data=dados_invalidos, apartamento=cenario_reserva['apartamento'])
    assert not form.is_valid()
    assert 'data_checkin' in form.errors


@pytest.mark.django_db
def test_reserva_form_conflito_de_datas_invalido(cenario_reserva):
    # ... (este teste continua igual) ...
    Reserva.objects.create(
        apartamento=cenario_reserva['apartamento'],
        hospede=cenario_reserva['hospede'],
        data_checkin='2025-09-10',
        data_checkout='2025-09-15'
    )
    dados_conflitantes = {'data_checkin': '2025-09-12', 'data_checkout': '2025-09-17'}
    form = ReservaForm(data=dados_conflitantes, apartamento=cenario_reserva['apartamento'])
    assert not form.is_valid()
    assert '__all__' in form.errors


@pytest.mark.django_db
def test_aprovar_reserva_service_falha_permissao(cenario_reserva):
    outro_usuario = User.objects.create_user(username='outro_usuario')
    reserva = Reserva.objects.create(
        apartamento=cenario_reserva['apartamento'],
        hospede=cenario_reserva['hospede'],
        data_checkin='2025-10-01',
        data_checkout='2025-10-05'
    )
    with pytest.raises(PermissionError, match="Usuário não tem permissão para aprovar esta reserva."):
        aprovar_reserva_service(reserva=reserva, usuario=outro_usuario)


@pytest.mark.django_db
def test_recusar_reserva_service_sucesso(cenario_reserva):
    reserva = Reserva.objects.create(
        apartamento=cenario_reserva['apartamento'],
        hospede=cenario_reserva['hospede'],
        data_checkin='2025-11-01',
        data_checkout='2025-11-05',
        status=Reserva.StatusReserva.PENDENTE
    )
    proprietario = cenario_reserva['proprietario']
    recusar_reserva_service(reserva=reserva, usuario=proprietario)
    reserva.refresh_from_db()
    assert reserva.status == Reserva.StatusReserva.CANCELADA


@pytest.mark.django_db
def test_recusar_reserva_service_falha_permissao(cenario_reserva):
    outro_usuario = User.objects.create_user(username='outro_usuario_2')
    reserva = Reserva.objects.create(
        apartamento=cenario_reserva['apartamento'],
        hospede=cenario_reserva['hospede'],
        data_checkin='2025-12-01',
        data_checkout='2025-12-05'
    )
    with pytest.raises(PermissionError, match="Usuário não tem permissão para recusar esta reserva."):
        recusar_reserva_service(reserva=reserva, usuario=outro_usuario)
from django.contrib.auth.models import User
from .models import Reserva

def aprovar_reserva_service(reserva: Reserva, usuario: User):
    """
    Executa a lógica de negócio para aprovar uma reserva.
    ... (código existente) ...
    """
    if usuario != reserva.apartamento.proprietario:
        raise PermissionError("Usuário não tem permissão para aprovar esta reserva.")

    reserva.status = Reserva.StatusReserva.CONFIRMADA
    reserva.save(update_fields=['status'])


# --- NOVA FUNÇÃO ABAIXO ---
def recusar_reserva_service(reserva: Reserva, usuario: User):
    """
    Executa a lógica de negócio para recusar uma reserva.

    :param reserva: A instância da Reserva a ser recusada.
    :param usuario: O usuário que está tentando executar a ação.
    :raises PermissionError: Se o usuário não for o proprietário do apartamento.
    """
    # Regra de Negócio: Apenas o proprietário pode recusar.
    if usuario != reserva.apartamento.proprietario:
        raise PermissionError("Usuário não tem permissão para recusar esta reserva.")

    # Ação Principal: Mudar o status.
    reserva.status = Reserva.StatusReserva.CANCELADA
    reserva.save(update_fields=['status'])
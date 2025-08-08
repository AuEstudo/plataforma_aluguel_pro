from django.core.mail import send_mail
from django.template.loader import render_to_string
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

    # --- LÓGICA DE E-MAIL ADICIONADA ---
    try:
        contexto_email = {
            'hospede': reserva.hospede,
            'apartamento': reserva.apartamento,
            'reserva': reserva,
        }
        corpo_email = render_to_string('emails/reserva_aprovada.txt', contexto_email)
        send_mail(
            subject=f'Sua reserva para "{reserva.apartamento.titulo}" foi APROVADA!',
            message=corpo_email,
            from_email='nao-responda@aluguelpro.com',
            recipient_list=[reserva.hospede.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"ERRO ao enviar e-mail de aprovação: {e}")


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

    # --- LÓGICA DE E-MAIL ADICIONADA ---
    try:
        contexto_email = {
            'hospede': reserva.hospede,
            'apartamento': reserva.apartamento,
            'reserva': reserva,
        }
        corpo_email = render_to_string('emails/reserva_recusada.txt', contexto_email)
        send_mail(
            subject=f'Atualização sobre sua reserva para "{reserva.apartamento.titulo}"',
            message=corpo_email,
            from_email='nao-responda@aluguelpro.com',
            recipient_list=[reserva.hospede.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"ERRO ao enviar e-mail de recusa: {e}")
# apartamentos/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    """
    Este backend de autenticação customizado permite que usuários
    façam login usando seu endereço de e-mail.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Tenta encontrar um usuário que corresponda ao username OU ao email (case-insensitive)
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # Se nenhum usuário for encontrado, retorna None para permitir que outros backends tentem.
            return None
        except UserModel.MultipleObjectsReturned:
            # Se múltiplos usuários forem encontrados (ex: mesmo username e email em contas diferentes,
            # o que não deveria acontecer se o email for único), retorna o primeiro.
            # Ou pode lançar um erro, dependendo da sua regra de negócio.
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        # Verifica a senha do usuário encontrado
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None # Senha incorreta

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
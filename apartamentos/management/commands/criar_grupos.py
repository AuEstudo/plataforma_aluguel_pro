# apartamentos/management/commands/criar_grupos.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apartamentos.models import Predio, Apartamento, Reserva

class Command(BaseCommand):
    help = 'Cria os grupos de usuários padrão e atribui permissões'

    def handle(self, *args, **kwargs):
        self.stdout.write("Criando grupos e atribuindo permissões...")

        # Modelos que proprietários podem gerenciar
        modelos_proprietario = [Predio, Apartamento, Reserva]

        # --- Grupo de Proprietários ---
        grupo_proprietarios, created = Group.objects.get_or_create(name='Proprietários')
        if created:
            self.stdout.write('Grupo "Proprietários" criado.')

        # Limpa permissões antigas para garantir consistência
        grupo_proprietarios.permissions.clear()

        for model in modelos_proprietario:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            # Adiciona todas as permissões (add, change, delete, view) para os modelos
            grupo_proprietarios.permissions.add(*permissions)

        self.stdout.write('Permissões para "Proprietários" atribuídas com sucesso.')

        # --- Grupo de Clientes ---
        grupo_clientes, created = Group.objects.get_or_create(name='Clientes')
        if created:
            self.stdout.write('Grupo "Clientes" criado.')

        grupo_clientes.permissions.clear()

        # Clientes podem adicionar e ver suas próprias reservas
        content_type_reserva = ContentType.objects.get_for_model(Reserva)
        perm_add_reserva = Permission.objects.get(codename='add_reserva', content_type=content_type_reserva)
        perm_view_reserva = Permission.objects.get(codename='view_reserva', content_type=content_type_reserva)
        grupo_clientes.permissions.add(perm_add_reserva, perm_view_reserva)

        self.stdout.write('Permissões para "Clientes" atribuídas com sucesso.')

        # (Futuramente, podemos adicionar os grupos Gerente e Funcionário aqui com suas permissões específicas)

        self.stdout.write(self.style.SUCCESS('Processo concluído!'))
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apartamentos.models import Predio, Apartamento, Reserva, Avaliacao


class Command(BaseCommand):
    help = 'Cria os grupos de usuários padrão (Proprietários, Clientes) e atribui as permissões corretas.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando a configuração de grupos e permissões...")

        # --- PERMISSÕES PARA O GRUPO DE CLIENTES ---
        grupo_clientes, created = Group.objects.get_or_create(name='Clientes')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Clientes" criado.'))

        permissoes_cliente_codenames = [
            'add_reserva',
            'view_reserva',
            'add_avaliacao',
        ]
        # Filtramos as permissões pelos seus 'codenames'
        permissoes_cliente = Permission.objects.filter(codename__in=permissoes_cliente_codenames)
        grupo_clientes.permissions.set(permissoes_cliente)
        self.stdout.write(self.style.SUCCESS('Permissões para "Clientes" atualizadas.'))

        # --- PERMISSÕES PARA O GRUPO DE PROPRIETÁRIOS ---
        grupo_proprietarios, created = Group.objects.get_or_create(name='Proprietários')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Proprietários" criado.'))

        permissoes_proprietario_codenames = [
            'add_predio', 'change_predio', 'delete_predio',
            'add_apartamento', 'change_apartamento', 'delete_apartamento',
            'view_reserva',
            'view_avaliacao',
        ]
        permissoes_proprietario = Permission.objects.filter(codename__in=permissoes_proprietario_codenames)
        grupo_proprietarios.permissions.set(permissoes_proprietario)
        self.stdout.write(self.style.SUCCESS('Permissões para "Proprietários" atualizadas.'))

        self.stdout.write(self.style.SUCCESS('Processo finalizado com sucesso!'))
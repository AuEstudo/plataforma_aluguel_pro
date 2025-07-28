from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apartamentos.models import Predio, Apartamento, Reserva

class Command(BaseCommand):
    help = 'Cria os grupos de usuários padrão (Proprietários, Clientes) e atribui as permissões corretas.'

    def handle(self, *args, **kwargs):
        # Criar grupo de Proprietários
        prop_group, created = Group.objects.get_or_create(name='Proprietários')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Proprietários" criado.'))
            # Permissões para proprietários
            perms_prop = Permission.objects.filter(
                codename__in=['add_predio', 'change_predio', 'delete_predio',
                              'add_apartamento', 'change_apartamento', 'delete_apartamento']
            )
            prop_group.permissions.set(perms_prop)
        else:
            self.stdout.write('Grupo "Proprietários" já existe.')

        # Criar grupo de Clientes
        cli_group, created = Group.objects.get_or_create(name='Clientes')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo "Clientes" criado.'))
            # Permissão para clientes fazerem reservas
            content_type = ContentType.objects.get_for_model(Reserva)
            perm_reserva, _ = Permission.objects.get_or_create(
                codename='add_reserva',
                name='Pode adicionar reserva',
                content_type=content_type
            )
            cli_group.permissions.add(perm_reserva)
        else:
            self.stdout.write('Grupo "Clientes" já existe.')

        self.stdout.write(self.style.SUCCESS('Processo de criação de grupos finalizado.'))
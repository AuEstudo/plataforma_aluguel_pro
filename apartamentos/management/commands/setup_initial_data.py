import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apartamentos.models import Comodidade

class Command(BaseCommand):
    help = 'Cria um superusuário e dados iniciais necessários para a produção.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando a configuração de dados iniciais...")

        # 1. Criação do Superusuário a partir de variáveis de ambiente
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        if not User.objects.filter(username=username).exists():
            if username and email and password:
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso.'))
            else:
                self.stdout.write(self.style.WARNING(
                    'Variáveis de ambiente do superusuário não configuradas. Pulando criação.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superusuário "{username}" já existe.'))

        # 2. Criação de Comodidades Padrão
        comodidades_padrao = ['Wi-Fi', 'Ar Condicionado', 'Cozinha Equipada', 'TV a Cabo', 'Estacionamento Gratuito']
        for nome_comodidade in comodidades_padrao:
            comodidade, created = Comodidade.objects.get_or_create(nome=nome_comodidade)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Comodidade "{nome_comodidade}" criada.'))

        self.stdout.write(self.style.SUCCESS('Configuração de dados iniciais finalizada.'))
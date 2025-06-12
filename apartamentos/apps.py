# apartamentos/apps.py
from django.apps import AppConfig

class ApartamentosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apartamentos'
    verbose_name = "Apartamentos e Imóveis"

    def ready(self):
        # Importa os sinais para que eles sejam registrados quando o app carregar.
        import apartamentos.signals
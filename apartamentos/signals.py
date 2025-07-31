# apartamentos/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil

@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Garante que um Perfil seja criado para cada novo User
    e que seja salvo sempre que o User for salvo.
    """
    if created:
        Perfil.objects.create(usuario=instance)
    # Garante que o perfil seja salvo junto com o usuário
    instance.perfil.save()
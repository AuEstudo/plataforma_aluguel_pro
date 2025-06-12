# apartamentos/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil

# O decorator @receiver conecta nossa função 'criar_perfil_usuario' ao sinal 'post_save'
# que é disparado pelo modelo 'User'.
@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """
    Cria um perfil para cada novo usuário cadastrado.
    """
    # 'created' é um booleano que é True apenas na primeira vez que o objeto é salvo.
    if created:
        Perfil.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    """
    Salva o perfil toda vez que o objeto User é salvo.
    """
    instance.perfil.save()
# apartamentos/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
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

@receiver(post_save, sender=Perfil)
def adicionar_usuario_ao_grupo(sender, instance, **kwargs):
    try:
        # Pega o grupo correspondente ao nome do cargo
        # Ex: se o cargo for 'PROPRIETARIO', busca o grupo 'Proprietários'
        cargo_nome = instance.get_cargo_display()  # Pega o nome legível, ex: "Proprietário"
        grupo, created = Group.objects.get_or_create(name=f'{cargo_nome}s')  # Adiciona 's' para plural

        # Remove o usuário de todos os outros grupos para garantir que ele tenha apenas um cargo
        instance.usuario.groups.clear()
        # Adiciona o usuário ao grupo correto
        instance.usuario.groups.add(grupo)
    except Group.DoesNotExist:
        print(
            f"AVISO: O grupo para o cargo '{instance.get_cargo_display()}' não existe. Rode 'python manage.py criar_grupos'.")
    except Exception as e:
        print(f"Ocorreu um erro no sinal adicionar_usuario_ao_grupo: {e}")
# config/settings/production.py
from .base import *

DEBUG = False

# IMPORTANTE: Quando você for colocar o site no ar, você deve colocar
# o seu domínio aqui. Ex: ['www.meusite.com.br']
ALLOWED_HOSTS = ['seu_dominio.com', 'www.seu_dominio.com']

# Configurações de segurança para produção (descomente quando tiver HTTPS)
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
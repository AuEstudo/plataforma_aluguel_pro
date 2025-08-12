import dj_database_url
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['plataforma-aluguel-pro.onrender.com']

# Configurações de segurança para produção (descomente quando tiver HTTPS)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Esta configuração lê a URL do banco de dados da variável de ambiente
# que o Render irá nos fornecer, tornando a configuração segura e flexível.
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}


STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
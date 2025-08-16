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

# ==============================================================================
# CONFIGURAÇÃO DE LOGGING PARA PRODUÇÃO
# ==============================================================================
# Esta configuração instrui o Django a enviar todos os erros (nível ERROR)
# para o console (stderr), que é o que o Render Logs captura.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# ==============================================================================
# CONFIGURAÇÃO DO CLOUDINARY PARA ARQUIVOS DE MÍDIA
# ==============================================================================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# Define o Cloudinary como o local de armazenamento padrão para arquivos de mídia
# apenas no ambiente de produção.
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

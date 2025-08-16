# config/settings/base.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Remova DEBUG e SECRET_KEY daqui, pois eles serão específicos de cada ambiente
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback_insecure_key')

# Lista de aplicativos instalados (comum a todos os ambientes)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    # Nossos Apps
    'apartamentos.apps.ApartamentosConfig',
    'django_filters',
    'django_cleanup.apps.CleanupConfig',
]

# Middlewares (comuns a todos os ambientes)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Banco de dados (pode ser sobrescrito no production.py)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ... (AUTH_PASSWORD_VALIDATORS, LANGUAGE_CODE, TIME_ZONE, etc. continuam aqui) ...
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
# ...

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT será definido no production.py

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = [
    'apartamentos.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
LOGIN_REDIRECT_URL = 'apartamentos:lista_apartamentos'
LOGOUT_REDIRECT_URL = 'homepage'
LOGIN_URL = 'login'
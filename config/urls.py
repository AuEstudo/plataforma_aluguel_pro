# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Nossas URLs de apartamentos
    path('', include('apartamentos.urls')), # Mudei para a raiz para ser a página principal

    # INCLUINDO AS URLS DE AUTENTICAÇÃO DO DJANGO
    # Isso cria automaticamente URLs como /accounts/login/, /accounts/logout/, etc.
    path('accounts/', include('django.contrib.auth.urls')),
]

# ... (o bloco 'if settings.DEBUG:' para media/static continua o mesmo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
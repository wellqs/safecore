"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import path, include

# Importações necessárias para servir arquivos estáticos em desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Adicionamos a configuração explícita para servir arquivos estáticos
if settings.DEBUG:
    # Esta linha diz ao Django: "Quando uma URL começar com /static/,
    # sirva os arquivos que estão no primeiro diretório listado em STATICFILES_DIRS".
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
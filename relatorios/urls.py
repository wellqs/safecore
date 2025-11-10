from django.urls import path
from . import views

app_name = "relatorios"

urlpatterns = [
    path("", views.home, name="home"),
    path("seguranca/", views.lista, {"categoria": "SEG"}, name="seguranca_lista"),
    path("saude/", views.lista, {"categoria": "SAU"}, name="saude_lista"),
    path("seguranca/novo/", views.criar, {"categoria": "SEG"}, name="seguranca_novo"),
    path("saude/novo/", views.criar, {"categoria": "SAU"}, name="saude_novo"),
    path("<int:pk>/editar/", views.editar, name="editar"),
    path("<int:pk>/excluir/", views.excluir, name="excluir"),
    path("<int:pk>/pdf/", views.exportar_pdf, name="pdf"),
]


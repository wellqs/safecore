from django.urls import path
from . import views

app_name = "notificacoes"

urlpatterns = [
    path("", views.NotificacaoListView.as_view(), name="lista"),
]


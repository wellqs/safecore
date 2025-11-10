from django.urls import path
from . import views

app_name = "treinamentos"

urlpatterns = [
    path("treinamentos/", views.TreinamentoListView.as_view(), name="treinamentos"),
    path("matriculas/", views.MatriculaListView.as_view(), name="matriculas"),
]


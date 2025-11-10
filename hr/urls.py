from django.urls import path
from . import views

app_name = "hr"

urlpatterns = [
    path("colaboradores/", views.ColaboradorListView.as_view(), name="colaboradores"),
    path("vinculos/", views.VinculoListView.as_view(), name="vinculos"),
]


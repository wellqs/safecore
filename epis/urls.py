from django.urls import path
from . import views

app_name = "epis"

urlpatterns = [
    path("catalogo/", views.EPIListView.as_view(), name="catalogo"),
    path("requisitos/", views.RequisitoListView.as_view(), name="requisitos"),
    path("entregas/", views.EntregaListView.as_view(), name="entregas"),
]


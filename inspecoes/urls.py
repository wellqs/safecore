from django.urls import path
from . import views

app_name = "inspecoes"

urlpatterns = [
    path("checklists/", views.ChecklistListView.as_view(), name="checklists"),
    path("inspecoes/", views.InspecaoListView.as_view(), name="inspecoes"),
    path("ncs/", views.NCListView.as_view(), name="ncs"),
]


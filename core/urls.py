# safecore/core/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # Rotas de Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Rota para a página inicial/dashboard
    path('', views.dashboard_view, name='dashboard'),

    # --- ROTAS DE FUNCIONÁRIOS ---
    # C(R)UD - Read (List)
    path('funcionarios/', views.listar_funcionarios_view, name='listar_funcionarios'),

    # (C)RUD - Create
    path('funcionarios/novo/', views.funcionario_create_view, name='funcionario_create'),

    # CR(U)D - Update
    path('funcionarios/<int:pk>/editar/', views.funcionario_update_view, name='funcionario_update'),

    # CRU(D) - Delete
    path('funcionarios/<int:pk>/excluir/', views.funcionario_delete_view, name='funcionario_delete'),

    # Rota para gerar o XML do eSocial S-2240 para um funcionário específico
    path('funcionarios/<int:pk>/gerar-s2240/', views.gerar_xml_s2240_view, name='gerar_xml_s2240'),

    # --- ROTAS DE GESTÃO DE RISCOS (PGR) ---
    path('pgr/ambientes/', views.listar_ambientes_view, name='listar_ambientes'),
    path('pgr/ambientes/novo/', views.ambiente_create_view, name='ambiente_create'),
    path('pgr/ges/', views.gerenciamento_ges_view, name='gerenciamento_ges'),

    path('pgr/cargos/', views.listar_cargos_view, name='listar_cargos'),
    path('pgr/cargos/novo/', views.cargo_create_view, name='cargo_create'),
    path('pgr/cargos/<int:pk>/editar/', views.cargo_update_view, name='cargo_update'),
    path('pgr/cargos/<int:pk>/excluir/', views.cargo_delete_view, name='cargo_delete'),

    # --- ALTERAÇÃO: Adicionada rota para EXCLUIR uma Exposição de Risco ---
    path('pgr/exposicao/<int:pk>/excluir/', views.exposicao_risco_delete_view, name='exposicao_risco_delete'),
]
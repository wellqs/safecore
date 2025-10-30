# safecore/core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# --- ALTERAÇÃO 1: Importar o 'messages' e o 'IntegrityError' ---
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.template import loader

from .models import Funcionario, ExposicaoRisco, Empresa, Aso, AmbienteDeTrabalho, Cargo, Risco
from .forms import FuncionarioForm, AmbienteDeTrabalhoForm, CargoForm, ExposicaoRiscoForm


@login_required
def dashboard_view(request):
    # ... (código existente sem alterações)
    today = timezone.now().date()
    thirty_days_from_now = today + timedelta(days=30)
    asos_a_vencer_count = Aso.objects.filter(
        vencimento__gte=today,
        vencimento__lte=thirty_days_from_now
    ).count()
    funcionarios_total_count = Funcionario.objects.count()
    empresas_total_count = Empresa.objects.count()
    context = {
        'asos_a_vencer_count': asos_a_vencer_count,
        'funcionarios_total_count': funcionarios_total_count,
        'empresas_total_count': empresas_total_count,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def gerar_xml_s2240_view(request, pk):
    # ... (código existente sem alterações)
    funcionario = get_object_or_404(Funcionario, pk=pk)
    exposicoes = ExposicaoRisco.objects.filter(
        cargo=funcionario.cargo
    ).select_related('risco', 'ambiente', 'ambiente__empresa')
    context = {
        'funcionario': funcionario,
        'exposicoes': exposicoes,
    }
    template = loader.get_template('core/s2240.xml')
    xml_content = template.render(context, request)
    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="S2240_{funcionario.cpf}.xml"'
    return response


@login_required
def listar_funcionarios_view(request):
    # ... (código existente sem alterações)
    funcionarios = Funcionario.objects.select_related('empresa', 'cargo').all()
    context = {
        'todos_os_funcionarios': funcionarios
    }
    return render(request, 'core/lista_funcionarios.html', context)


@login_required
def funcionario_create_view(request):
    # ... (código existente sem alterações)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:listar_funcionarios')
    else:
        form = FuncionarioForm()
    context = {
        'form': form,
        'page_title': 'Adicionar Novo Funcionário'
    }
    return render(request, 'core/form_funcionario.html', context)


@login_required
def funcionario_update_view(request, pk):
    # ... (código existente sem alterações)
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            return redirect('core:listar_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)
    context = {
        'form': form,
        'page_title': f'Editar Funcionário: {funcionario.nome_completo}'
    }
    return render(request, 'core/form_funcionario.html', context)


@login_required
def funcionario_delete_view(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('core:listar_funcionarios')

    context = {
        'object': funcionario,
        'cancel_url': reverse('core:listar_funcionarios')
    }
    return render(request, 'core/confirmar_exclusao.html', context)


@login_required
def listar_ambientes_view(request):
    # ... (código existente sem alterações)
    ambientes = AmbienteDeTrabalho.objects.select_related('empresa').all()

    context = {
        'todos_os_ambientes': ambientes
    }
    return render(request, 'core/lista_ambientes.html', context)


@login_required
def ambiente_create_view(request):
    # ... (código existente sem alterações)
    if request.method == 'POST':
        form = AmbienteDeTrabalhoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:listar_ambientes')
    else:
        form = AmbienteDeTrabalhoForm()

    context = {
        'form': form,
        'page_title': 'Adicionar Novo Ambiente de Trabalho'
    }
    return render(request, 'core/form_ambientes.html', context)


@login_required
def ambiente_update_view(request, pk):
    ambiente = get_object_or_404(AmbienteDeTrabalho, pk=pk)
    if request.method == 'POST':
        form = AmbienteDeTrabalhoForm(request.POST, instance=ambiente)
        if form.is_valid():
            form.save()
            return redirect('core:listar_ambientes')
    else:
        form = AmbienteDeTrabalhoForm(instance=ambiente)
    context = {
        'form': form,
        'page_title': f'Editar Ambiente: {ambiente.nome}'
    }
    return render(request, 'core/form_ambientes.html', context)


@login_required
def ambiente_delete_view(request, pk):
    ambiente = get_object_or_404(AmbienteDeTrabalho, pk=pk)
    if request.method == 'POST':
        ambiente.delete()
        return redirect('core:listar_ambientes')
    context = {
        'object': ambiente,
        'cancel_url': reverse('core:listar_ambientes')
    }
    return render(request, 'core/confirmar_exclusao.html', context)


@login_required
def listar_cargos_view(request):
    # ... (código existente sem alterações)
    cargos = Cargo.objects.all().order_by('nome')
    context = {
        'todos_os_cargos': cargos
    }
    return render(request, 'core/lista_cargos.html', context)


@login_required
def cargo_create_view(request):
    # ... (código existente sem alterações)
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:listar_cargos')
    else:
        form = CargoForm()
    context = {
        'form': form,
        'page_title': 'Adicionar Novo Cargo'
    }
    return render(request, 'core/form_cargos.html', context)


@login_required
def cargo_update_view(request, pk):
    # ... (código existente sem alterações)
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('core:listar_cargos')
    else:
        form = CargoForm(instance=cargo)
    context = {
        'form': form,
        'page_title': f'Editar Cargo: {cargo.nome}'
    }
    return render(request, 'core/form_cargos.html', context)


@login_required
def cargo_delete_view(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        cargo.delete()
        return redirect('core:listar_cargos')
    context = {
        'object': cargo,
        'cancel_url': reverse('core:listar_cargos')
    }
    return render(request, 'core/confirmar_exclusao.html', context)


# --- ALTERAÇÃO 3: View 'gerenciamento_ges_view' substituída pela versão robusta ---
@login_required
def gerenciamento_ges_view(request):
    """
    View para gerenciar as Exposições de Risco por Grupo de Exposição Similar (GES).
    """
    todos_os_cargos = Cargo.objects.all().order_by('nome')
    todos_os_ambientes = AmbienteDeTrabalho.objects.all().order_by('nome')

    selected_cargo_id = request.GET.get('cargo_id')
    selected_ambiente_id = request.GET.get('ambiente_id')

    exposicoes_do_ges = None
    selected_cargo = None
    selected_ambiente = None
    form = ExposicaoRiscoForm()

    if selected_cargo_id and selected_ambiente_id:
        selected_cargo = get_object_or_404(Cargo, pk=selected_cargo_id)
        selected_ambiente = get_object_or_404(AmbienteDeTrabalho, pk=selected_ambiente_id)

        if request.method == 'POST':
            form = ExposicaoRiscoForm(request.POST)
            if form.is_valid():
                nova_exposicao = form.save(commit=False)
                nova_exposicao.cargo = selected_cargo
                nova_exposicao.ambiente = selected_ambiente

                # Bloco try...except para tratar o erro de duplicidade
                try:
                    nova_exposicao.save()
                    messages.success(request, f"Risco '{nova_exposicao.risco.nome}' adicionado ao GES com sucesso!")
                except IntegrityError:
                    messages.error(request,
                                   f"Erro: O risco '{nova_exposicao.risco.nome}' já está cadastrado para este GES.")

                return redirect(f"{request.path}?cargo_id={selected_cargo_id}&ambiente_id={selected_ambiente_id}")

        exposicoes_do_ges = ExposicaoRisco.objects.filter(
            cargo_id=selected_cargo_id,
            ambiente_id=selected_ambiente_id
        ).select_related('risco')

    context = {
        'todos_os_cargos': todos_os_cargos,
        'todos_os_ambientes': todos_os_ambientes,
        'selected_cargo_id': int(selected_cargo_id) if selected_cargo_id else None,
        'selected_ambiente_id': int(selected_ambiente_id) if selected_ambiente_id else None,
        'selected_cargo': selected_cargo,
        'selected_ambiente': selected_ambiente,
        'exposicoes_do_ges': exposicoes_do_ges,
        'form': form,
    }

    return render(request, 'core/gerenciamento_ges.html', context)


@login_required
def exposicao_risco_delete_view(request, pk):
    # ... (código existente sem alterações)
    exposicao = get_object_or_404(ExposicaoRisco, pk=pk)
    cargo_id = exposicao.cargo.id
    ambiente_id = exposicao.ambiente.id

    if request.method == 'POST':
        exposicao.delete()
        return redirect(f"{reverse('core:gerenciamento_ges')}?cargo_id={cargo_id}&ambiente_id={ambiente_id}")

    context = {
        'object': f"Risco '{exposicao.risco.nome}' para o cargo '{exposicao.cargo.nome}'",
        'cancel_url': reverse('core:gerenciamento_ges') + f'?cargo_id={cargo_id}&ambiente_id={ambiente_id}',
    }
    return render(request, 'core/confirmar_exclusao.html', context)
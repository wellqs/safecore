from datetime import date
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Relatorio, RelatorioAtividade
from .forms import RelatorioForm, RelatorioAtividadeFormSet


SEGURANCA_ATIVIDADES = [
    # 1. Gestão de Riscos e Inspeções
    "Elaboração/revisão/atualização do PGR",
    "Levantamento de perigos e riscos por setor",
    "Identificação de riscos (fís., quim., biol., erg., mec.)",
    "Avaliação de probabilidade e severidade",
    "Inspeções de segurança (rotineiras/periódicas)",
    "Verificação de condições e atos inseguros",
    "Relatórios de inspeção (fotos/NC/prazos)",
    "Monitoramento do plano de ações",
    # 2. EPIs
    "Controle de estoque e validade de EPIs",
    "Entrega/recebimento com assinatura digital",
    "Adequação dos EPIs aos riscos",
    "Substituição de EPIs danificados/vencidos",
    "Treinamentos de uso/conservação/guarda de EPIs",
    "Acompanhamento do CA dos EPIs",
    # 3. Treinamentos e Capacitações
    "Planejamento/execução de treinamentos das NRs",
    "Integração de novos colaboradores",
    "Reciclagens/capacitações internas",
    "Registro de participação/carga/validade",
    "Avaliação de eficácia do treinamento",
    # 4. Emergência e Brigada
    "Manutenção/inspeção de extintores/hidrantes/alarmes",
    "Capacitação da Brigada de Incêndio",
    "Simulados de evacuação/combate a incêndio",
    "Planos de emergência e abandono",
    "Rota de fuga e sinalização",
    "Relatórios de vistoria do Corpo de Bombeiros",
    # 5. Elétrica e Máquinas
    "Conformidade de instalações elétricas (NR-10)",
    "Inspeção de máquinas (NR-12)",
    "Laudos de Conformidade e ARTs",
    "Análise de riscos em altura e espaços confinados",
    "Permissões de trabalho e LOTO",
    # 6. Acidentes e Incidentes
    "Registro/investigação de acidentes e quase-acidentes",
    "Aplicação de 5 Porquês/Árvore de Causas",
    "Causas imediatas e raízes",
    "Ações corretivas e preventivas",
    "Emissão/controle de CAT",
    "Indicadores: frequência/gravidade/incidentes",
    # 7. Sinalização e Condições Ambientais
    "Verificação de sinalização e faixas",
    "Avaliação ergonômica (AET - NR-17)",
    "Melhorias de posturas/mobiliários/layout",
    "Iluminação/ventilação/ruído",
    "Condições de higiene/limpeza/conforto",
    # 8. Documentação e Conformidade
    "Atualização e controle (PGR/PCMSO/LTCAT/PPP/EPI/Treinamentos)",
    "Controle de prazos de programas e laudos",
    "Acompanhamento de auditorias",
    "Planos de ação pós-fiscalização",
]


SAUDE_ATIVIDADES = [
    # 1. PCMSO
    "Coordenação do PCMSO",
    "Exames Admissional/Periódico/Retorno/Mudança/Demissional",
    "Registro/arquivamento de ASOs",
    "Acompanhamento de restrições e readaptações",
    "Análise de afastamentos e doenças ocupacionais",
    # 2. Vigilância em Saúde do Trabalhador
    "Investigação de doenças relacionadas ao trabalho",
    "Notificações SINAN",
    "Avaliação epidemiológica e indicadores",
    "Ações preventivas de saúde ocupacional",
    # 3. Promoção da Saúde
    "Campanhas de vacinação",
    "Conscientização (SIPAT, Outubro Rosa, etc.)",
    "Ginástica laboral / ergonomia ativa",
    "Acompanhamento nutricional/psicológico",
    "Palestras/campanhas educativas",
    # 4. Afastamentos e Reabilitação
    "Controle de afastamentos e atestados",
    "Comunicação com INSS e benefícios",
    "Reintegração e readaptação",
    "Relatórios de absenteísmo",
    # 5. Saúde Mental
    "Monitoramento de estresse/burnout/fadiga",
    "Encaminhamentos e acolhimento",
    "Protocolos contra assédio/violência",
    # 6. Ambientes Hospitalares (NR-32)
    "Acidentes com material biológico",
    "Gestão de vacinação obrigatória",
    "Monitoramento de exposição a agentes",
    "Treinamentos de biossegurança",
    "Resíduos de saúde (PGRSS)",
]


def _atividades_padrao(categoria: str):
    return SEGURANCA_ATIVIDADES if categoria == Relatorio.Categoria.SEGURANCA else SAUDE_ATIVIDADES


@login_required
def home(request):
    return render(request, "relatorios/home.html")


@login_required
def lista(request, categoria: str):
    qs = Relatorio.objects.filter(categoria=categoria)
    return render(request, "relatorios/lista.html", {
        "categoria": categoria,
        "categoria_nome": dict(Relatorio.Categoria.choices).get(categoria, categoria),
        "object_list": qs,
    })


def _ensure_atividades(rel: Relatorio):
    if rel.atividades.exists():
        return
    base = _atividades_padrao(rel.categoria)
    for i, nome in enumerate(base, start=1):
        RelatorioAtividade.objects.create(relatorio=rel, nome=nome, ordem=i, contador=0)


@login_required
def criar(request, categoria: str):
    # Página de criação com lista de atividades padrão e contadores.
    atividades_nomes = _atividades_padrao(categoria)
    initial = {"data": date.today()}
    if request.method == "POST":
        form = RelatorioForm(request.POST)
        if form.is_valid():
            rel: Relatorio = form.save(commit=False)
            rel.categoria = categoria
            rel.save()
            # criar atividades com base nos contadores enviados
            for i, nome in enumerate(atividades_nomes, start=0):
                valor = request.POST.get(f"contador_{i}")
                try:
                    contador = int(valor) if valor is not None else 0
                except ValueError:
                    contador = 0
                RelatorioAtividade.objects.create(relatorio=rel, nome=nome, ordem=i + 1, contador=max(0, contador))
            messages.success(request, "Relatório salvo com sucesso.")
            if categoria == Relatorio.Categoria.SEGURANCA:
                return redirect("relatorios:seguranca_lista")
            else:
                return redirect("relatorios:saude_lista")
    else:
        form = RelatorioForm(initial=initial)
    return render(
        request,
        "relatorios/novo.html",
        {
            "form": form,
            "categoria": categoria,
            "categoria_nome": dict(Relatorio.Categoria.choices).get(categoria),
            "atividades": list(enumerate(atividades_nomes)),  # (index, nome)
        },
    )


@login_required
def editar(request, pk: int):
    rel = get_object_or_404(Relatorio, pk=pk)
    _ensure_atividades(rel)
    if request.method == "POST":
        form = RelatorioForm(request.POST, instance=rel)
        formset = RelatorioAtividadeFormSet(request.POST, instance=rel)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Relatório salvo com sucesso.")
            if rel.categoria == Relatorio.Categoria.SEGURANCA:
                return redirect("relatorios:seguranca_lista")
            else:
                return redirect("relatorios:saude_lista")
    else:
        form = RelatorioForm(instance=rel)
        formset = RelatorioAtividadeFormSet(instance=rel)
    return render(request, "relatorios/form.html", {"form": form, "formset": formset, "relatorio": rel, "categoria_nome": rel.get_categoria_display()})


@login_required
def excluir(request, pk: int):
    rel = get_object_or_404(Relatorio, pk=pk)
    if request.method == "POST":
        categoria = rel.categoria
        rel.delete()
        messages.success(request, "Relatório excluído.")
        if categoria == Relatorio.Categoria.SEGURANCA:
            return redirect("relatorios:seguranca_lista")
        else:
            return redirect("relatorios:saude_lista")
    return render(request, "relatorios/confirmar_exclusao.html", {"object": rel})


@login_required
def exportar_pdf(request, pk: int):
    rel = get_object_or_404(Relatorio, pk=pk)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename=relatorio_{rel.id}.pdf"
        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 2 * cm
        p.setFont("Helvetica-Bold", 14)
        p.drawString(2 * cm, y, f"{rel.get_categoria_display()} - {rel.titulo}")
        y -= 0.8 * cm
        p.setFont("Helvetica", 11)
        p.drawString(2 * cm, y, f"Data: {rel.data.strftime('%d/%m/%Y')}")
        y -= 1 * cm
        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y, "Atividades")
        y -= 0.6 * cm
        p.setFont("Helvetica", 10)
        for at in rel.atividades.all():
            linha = f"- {at.nome}: {at.contador}"
            if y < 2 * cm:
                p.showPage(); y = height - 2 * cm; p.setFont("Helvetica", 10)
            p.drawString(2 * cm, y, linha)
            y -= 0.5 * cm
        y -= 0.5 * cm
        p.setFont("Helvetica-Bold", 12)
        p.drawString(2 * cm, y, "Observação")
        y -= 0.6 * cm
        p.setFont("Helvetica", 10)
        for line in (rel.observacao or "-").splitlines() or ["-"]:
            if y < 2 * cm:
                p.showPage(); y = height - 2 * cm; p.setFont("Helvetica", 10)
            p.drawString(2 * cm, y, line)
            y -= 0.5 * cm
        p.showPage()
        p.save()
        return response
    except Exception:
        # Fallback simples: HTML imprimível
        html = render(request, "relatorios/pdf_fallback.html", {"relatorio": rel}).content
        resp = HttpResponse(html, content_type="text/html")
        resp["Content-Disposition"] = f"inline; filename=relatorio_{rel.id}.html"
        return resp

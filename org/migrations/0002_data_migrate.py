from django.db import migrations


def forwards(apps, schema_editor):
    CoreEmpresa = apps.get_model('core', 'Empresa')
    CoreAmbiente = apps.get_model('core', 'AmbienteDeTrabalho')

    Empresa = apps.get_model('org', 'Empresa')
    Unidade = apps.get_model('org', 'Unidade')
    Setor = apps.get_model('org', 'Setor')
    Funcao = apps.get_model('org', 'Funcao')
    AmbienteTrabalho = apps.get_model('org', 'AmbienteTrabalho')
    CoreCargo = apps.get_model('core', 'Cargo')

    empresa_map = {}
    for ce in CoreEmpresa.objects.all():
        e, _ = Empresa.objects.get_or_create(
            cnpj=ce.cnpj,
            defaults={
                'razao_social': ce.razao_social,
                'nome_fantasia': ce.nome_fantasia,
            }
        )
        empresa_map[ce.id] = e
        unidade, _ = Unidade.objects.get_or_create(empresa=e, nome='Unidade Padrão')
        setor, _ = Setor.objects.get_or_create(unidade=unidade, nome='Setor Padrão')

    funcao_map = {}
    for cc in CoreCargo.objects.all():
        # Coloca todas as funções no Setor Padrão da primeira unidade da primeira empresa encontrada
        # ou tenta associar pela primeira empresa existente
        # Estratégia simples: usa a primeira Empresa criada
        first_emp = next(iter(empresa_map.values()), None)
        if first_emp is None:
            continue
        unidade = Unidade.objects.filter(empresa=first_emp, nome='Unidade Padrão').first()
        setor = Setor.objects.filter(unidade=unidade, nome='Setor Padrão').first()
        f, _ = Funcao.objects.get_or_create(setor=setor, nome=cc.nome, defaults={'descricao': cc.descricao})
        funcao_map[cc.id] = f

    for ca in CoreAmbiente.objects.all():
        e = empresa_map.get(ca.empresa_id)
        if not e:
            continue
        unidade = Unidade.objects.filter(empresa=e, nome='Unidade Padrão').first()
        AmbienteTrabalho.objects.get_or_create(
            unidade=unidade,
            nome=ca.nome,
            defaults={'descricao': ca.descricao}
        )


def backwards(apps, schema_editor):
    # Não reverte dados
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('org', '0001_initial'),
        ('core', '0003_popular_tabelas_sst'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]


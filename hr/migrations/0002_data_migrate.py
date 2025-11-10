from django.db import migrations


def forwards(apps, schema_editor):
    CoreFuncionario = apps.get_model('core', 'Funcionario')
    CoreCargo = apps.get_model('core', 'Cargo')

    Empresa = apps.get_model('org', 'Empresa')
    Unidade = apps.get_model('org', 'Unidade')
    Setor = apps.get_model('org', 'Setor')
    Funcao = apps.get_model('org', 'Funcao')

    Colaborador = apps.get_model('hr', 'Colaborador')
    Vinculo = apps.get_model('hr', 'Vinculo')

    # Indexes auxiliares
    funcao_by_cargo = { }
    for f in Funcao.objects.all():
        funcao_by_cargo[f.nome] = f

    for cf in CoreFuncionario.objects.all():
        empresa = Empresa.objects.filter(cnpj=cf.empresa.cnpj).first()
        if not empresa:
            continue
        unidade = Unidade.objects.filter(empresa=empresa, nome='Unidade Padrão').first()
        setor = Setor.objects.filter(unidade=unidade, nome='Setor Padrão').first()
        funcao = funcao_by_cargo.get(cf.cargo.nome)
        if not funcao:
            # fallback: cria função no setor padrão
            funcao = Funcao.objects.create(setor=setor, nome=cf.cargo.nome, descricao=getattr(cf.cargo, 'descricao', None))

        colab, _ = Colaborador.objects.get_or_create(
            cpf=cf.cpf,
            defaults={
                'empresa': empresa,
                'nome_completo': cf.nome_completo,
                'data_nascimento': None,
                'pis': None,
            }
        )
        Vinculo.objects.get_or_create(
            colaborador=colab,
            funcao=funcao,
            unidade=unidade,
            setor=setor,
            data_admissao=cf.data_admissao,
            defaults={'ativo': True}
        )


def backwards(apps, schema_editor):
    # Não reverte dados
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('hr', '0001_initial'),
        ('org', '0002_data_migrate'),
        ('core', '0003_popular_tabelas_sst'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]


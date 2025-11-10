from django.db import migrations


def forwards(apps, schema_editor):
    CoreRisco = apps.get_model('core', 'Risco')
    CoreExposicaoRisco = apps.get_model('core', 'ExposicaoRisco')
    CoreCargo = apps.get_model('core', 'Cargo')
    CoreAmbiente = apps.get_model('core', 'AmbienteDeTrabalho')

    Risco = apps.get_model('pgr', 'Risco')
    MapaExposicao = apps.get_model('pgr', 'MapaExposicao')

    Funcao = apps.get_model('org', 'Funcao')
    Unidade = apps.get_model('org', 'Unidade')
    AmbienteTrabalho = apps.get_model('org', 'AmbienteTrabalho')

    # Migrar riscos (tabela 24)
    risco_map = {}
    for cr in CoreRisco.objects.all():
        r, _ = Risco.objects.get_or_create(
            codigo_esocial=cr.codigo_esocial,
            defaults={
                'nome': cr.nome,
                'tipo': cr.tipo,
                'descricao': cr.descricao,
            }
        )
        risco_map[cr.id] = r

    # Migrar exposições por função/ambiente
    for ce in CoreExposicaoRisco.objects.all():
        funcao = Funcao.objects.filter(nome=ce.cargo.nome).first()
        # Ambiente: buscar pelo nome dentro da mesma empresa (via unidade padrão)
        # Primeiro, encontrar a unidade padrão da empresa desse ambiente
        unidade = Unidade.objects.filter(empresa__cnpj=ce.ambiente.empresa.cnpj, nome='Unidade Padrão').first()
        ambiente = AmbienteTrabalho.objects.filter(unidade=unidade, nome=ce.ambiente.nome).first()
        risco = risco_map.get(ce.risco_id)
        if funcao and ambiente and risco:
            MapaExposicao.objects.get_or_create(
                funcao=funcao,
                ambiente=ambiente,
                risco=risco,
                defaults={
                    'intensidade': ce.intensidade,
                    'tecnica_utilizada': ce.tecnica_utilizada,
                }
            )


def backwards(apps, schema_editor):
    # Não reverte dados
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('pgr', '0002_mapaexposicao_mapaexposicao_unique_mapa_exposicao'),
        ('org', '0002_data_migrate'),
        ('core', '0003_popular_tabelas_sst'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]


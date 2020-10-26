from django.db import migrations


def create_positions(apps, schema_editor):
    positions = {
        "Golero": "GOL",
        "Carrilero izquierdo": "DEF",
        "Carrilero derecho": "DEF",
        "Lateral izquierdo": "DEF",
        "Lateral derecho": "DEF",
        "Central izquierdo": "DEF",
        "Central derecho": "DEF",
        "Central": "DEF",
        "Mediocampista defensivo": "MED",
        "Interior izquierdo": "MED",
        "Mediocentro izquierdo": "MED",
        "Mediocentro derecho": "MED",
        "Interior derecho": "MED",
        "Media punta": "MED",
        "Delantero central": "DEL",
        "Volante izquierdo": "DEL",
        "Volante delantero": "DEL",
        "Segunda punta": "DEL",
        "Centro delantero": "DEL",
        "Extremo izquierdo": "DEL",
        "Extremo derecho": "DEL",
        "Director técnico": "DIR",
    }
    position = apps.get_model('formation', 'Position')
    for k, v in positions.items():
        position(position_name=k, type=v).save()


class Migration(migrations.Migration):
    dependencies = [
        ('formation', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_positions)
    ]

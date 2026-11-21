from django.db import migrations


def crear_escenario_ejemplo(apps, schema_editor):
    Escenario = apps.get_model("ocupacion", "Escenario")
    Escenario.objects.using(schema_editor.connection.alias).get_or_create(
        nombre="Salón 101",
        defaults={
            "estados": ["Libre", "Medio", "Lleno"],
            "matriz": [
                [0.50, 0.35, 0.15],
                [0.25, 0.45, 0.30],
                [0.10, 0.35, 0.55],
            ],
        },
    )


def eliminar_escenario_ejemplo(apps, schema_editor):
    Escenario = apps.get_model("ocupacion", "Escenario")
    Escenario.objects.using(schema_editor.connection.alias).filter(
        nombre="Salón 101"
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("ocupacion", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(crear_escenario_ejemplo, eliminar_escenario_ejemplo),
    ]

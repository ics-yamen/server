# Generated by Django 3.2.25 on 2024-07-16 09:43

from django.db import migrations, models


def delete_ids(apps, schema_editor):
    AutomaticSummary = apps.get_model('analysis', 'AutomaticSummary')
    AutomaticSummary.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0015_auto_20240531_0504'),
    ]

    operations = [
        migrations.RunPython(
            delete_ids,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AddField(
            model_name='automaticsummary',
            name='analytical_statement',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='automaticsummary',
            name='information_gap',
            field=models.TextField(blank=True),
        ),
    ]

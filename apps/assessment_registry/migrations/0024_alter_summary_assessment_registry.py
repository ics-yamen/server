# Generated by Django 3.2.17 on 2023-08-10 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessment_registry', '0023_alter_assessmentregistry_protection_info_mgmts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summary',
            name='assessment_registry',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='summary', to='assessment_registry.assessmentregistry'),
        ),
    ]

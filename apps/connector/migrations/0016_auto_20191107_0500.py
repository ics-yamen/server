# Generated by Django 2.1.13 on 2019-11-07 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0015_remove_connector_source'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connector',
            old_name='source_obj',
            new_name='source',
        ),
    ]
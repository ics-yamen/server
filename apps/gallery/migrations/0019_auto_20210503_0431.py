# Generated by Django 3.2 on 2021-05-03 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0018_auto_20191217_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='metadata',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='filepreview',
            name='ngrams',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]

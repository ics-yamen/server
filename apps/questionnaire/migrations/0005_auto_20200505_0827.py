# Generated by Django 2.1.15 on 2020-05-05 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_auto_20200504_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='crisis_type',
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='crisis_types',
            field=models.ManyToManyField(blank=True, to='questionnaire.CrisisType'),
        ),
    ]

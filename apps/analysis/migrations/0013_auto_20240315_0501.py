# Generated by Django 3.2.17 on 2024-03-15 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0012_remove_analysisreportcontainer_content_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyticalstatement',
            name='title',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='topicmodelcluster',
            name='title',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]

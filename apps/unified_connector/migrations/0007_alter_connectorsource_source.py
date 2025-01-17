# Generated by Django 3.2.12 on 2022-06-21 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unified_connector', '0006_alter_connectorsource_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectorsource',
            name='source',
            field=models.CharField(choices=[('atom-feed', 'Atom Feed'), ('relief-web', 'Relifweb'), ('rss-feed', 'RSS Feed'), ('unhcr-portal', 'UNHCR Portal'), ('humanitarian-resp', 'Humanitarian Response'), ('pdna', 'Post Disaster Needs Assessments'), ('emm', 'European Media Monitor')], max_length=20),
        ),
    ]

# Generated by Django 3.2.17 on 2023-07-19 09:34

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment_registry', '0002_auto_20230710_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmentregistry',
            name='focuses',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(0, 'Context'), (1, 'Shock/Event'), (2, 'Displacement'), (3, 'Casualties'), (4, 'Information and Communication'), (5, 'Humaniterian Access'), (6, 'Impact'), (7, 'Humanitarian Conditions'), (8, 'People at risk'), (9, 'Priorities & Preferences'), (10, 'Response and Capacities')]), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='assessmentregistry',
            name='sectors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(0, 'Food Security'), (1, 'Heath'), (2, 'Shelter'), (3, 'Wash'), (4, 'Protection'), (5, 'Nutrition'), (6, 'Livelihood'), (7, 'Education'), (8, 'Logistics'), (9, 'Inter/Cross Sector')]), default=list, size=None),
        ),
    ]
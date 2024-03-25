# Generated by Django 3.2.17 on 2023-12-20 10:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment_registry', '0042_alter_assessmentregistry_affected_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmentregistry',
            name='focuses',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(1, 'Context'), (2, 'Shock/Event'), (3, 'Displacement'), (4, 'Casualties'), (5, 'Information & Communication'), (6, 'Humanitarian Access'), (7, 'Impact (scope & Scale)'), (8, 'Humanitarian Conditions'), (9, 'People at risk'), (10, 'Priorities & Preferences'), (11, 'Response & Capacities')]), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='assessmentregistry',
            name='sectors',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(1, 'Food Security'), (2, 'Health'), (3, 'Shelter'), (4, 'Wash'), (5, 'Protection'), (6, 'Nutrition'), (7, 'Livelihood'), (8, 'Education'), (9, 'Logistics'), (10, 'Inter/Cross Sector')]), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='scoreanalyticaldensity',
            name='analysis_level_covered',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(1, 'Issues/unmet needs are detailed'), (2, 'Issues/unmet needs are prioritized/ranked'), (3, 'Causes or underlying mechanisms behind issues/unmet needs are detailed'), (4, 'Causes or underlying mechanisms behind issues/unmet needs are prioritized/ranked'), (5, 'Severity of some/all issues/unmet_needs_is_detailed'), (6, 'Future issues/unmet needs are detailed'), (7, 'Future issues/unmet needs are prioritized/ranked'), (8, 'Severity of some/all future issues/unmet_needs_is_detailed'), (9, 'Recommendations/interventions are detailed'), (10, 'Recommendations/interventions are prioritized/ranked')]), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='scoreanalyticaldensity',
            name='figure_provided',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(choices=[(1, 'Total population in the assessed areas'), (2, 'Total population exposed to the shock/event'), (3, 'Total population affected/living in the affected area'), (4, 'Total population facing humanitarian access constraints'), (5, 'Total population in need'), (6, 'Total population in critical need'), (7, 'Total population in severe need'), (8, 'Total population in moderate need'), (9, 'Total population at risk/vulnerable'), (10, 'Total population reached by assistance')]), blank=True, default=list, size=None),
        ),
    ]
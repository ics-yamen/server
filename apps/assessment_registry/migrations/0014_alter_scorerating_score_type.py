# Generated by Django 3.2.17 on 2023-08-03 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment_registry', '0013_auto_20230803_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scorerating',
            name='score_type',
            field=models.IntegerField(choices=[(0, 'Relevance'), (1, 'Comprehensiveness'), (2, 'Timeliness'), (3, 'Granularity'), (4, 'Comparability'), (5, 'Source reability'), (6, 'Methods'), (7, 'Triangulation'), (8, 'Plausibility'), (9, 'Inclusiveness'), (10, 'Assumptions'), (11, 'Corroboration'), (12, 'Structured Ananlytical Technique'), (13, 'Consensus'), (14, 'Reproducibility'), (15, 'Clearly Articulated Result'), (16, 'Level Of Confidence'), (17, 'Illustration'), (18, 'Sourced data and evidence'), (19, 'Clearly stated outliers')]),
        ),
    ]
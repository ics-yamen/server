# Generated by Django 2.1.15 on 2020-05-04 09:52

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0003_question_is_archived_squashed_0010_auto_20200217_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='data_collection_technique',
        ),
        migrations.AddField(
            model_name='frameworkquestion',
            name='more_titles',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='more_titles',
            field=django.contrib.postgres.fields.hstore.HStoreField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='data_collection_techniques',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('direct', 'Direct observation'), ('focus_group', 'Focus group'), ('one_on_one_interviews', '1-on-1 interviews'), ('open_ended_survey', 'Open-ended survey'), ('closed_ended_survey', 'Closed-ended survey')], max_length=56), default=list, size=None),
        ),
    ]

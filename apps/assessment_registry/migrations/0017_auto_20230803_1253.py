# Generated by Django 3.2.17 on 2023-08-03 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assessment_registry', '0016_alter_assessmentregistry_protection_info_mgmts'),
    ]

    operations = [
        migrations.CreateModel(
            name='SummarySubDimmensionIssue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('client_id', models.CharField(blank=True, default=None, max_length=128, null=True, unique=True)),
                ('focus', models.IntegerField(choices=[(0, 'Food Security'), (1, 'Heath'), (2, 'Shelter'), (3, 'Wash'), (4, 'Protection'), (5, 'Nutrition'), (6, 'Livelihood'), (7, 'Education'), (8, 'Logistics'), (9, 'Inter/Cross Sector')])),
                ('text', models.TextField(blank=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('lead_preview_text_ref', models.JSONField(blank=True, default=None, null=True)),
                ('assessment_registry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='summary_focus_subsector_issue_ary', to='assessment_registry.assessmentregistry')),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='summarysubdimmensionissue_created', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='summarysubdimmensionissue_modified', to=settings.AUTH_USER_MODEL)),
                ('summary_issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='summary_focus_subsector_issue', to='assessment_registry.summaryissue')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='scoreanalyticaldensity',
            name='figure_provided',
        ),
        migrations.DeleteModel(
            name='SummaryFocusSubSectorIssue',
        ),
    ]

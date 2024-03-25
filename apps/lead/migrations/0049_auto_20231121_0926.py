# Generated by Django 3.2.17 on 2023-11-21 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lead', '0048_auto_20230228_0810'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='auto_entry_extraction_status',
            field=models.SmallIntegerField(choices=[(0, 'Pending'), (1, 'Success'), (2, 'Failed')], default=0),
        ),
        migrations.CreateModel(
            name='ExtractedLead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('client_id', models.CharField(blank=True, default=None, max_length=128, null=True, unique=True)),
                ('entry_extraction_classification', models.TextField()),
                ('text_extraction_id', models.CharField(blank=True, max_length=50, null=True)),
                ('text_extraction_status', models.IntegerField(choices=[(1, 'Initiated'), (2, 'Success'), (3, 'Failed'), (4, 'Input url process failed')], default=1)),
                ('text_classification_status', models.IntegerField(choices=[(1, 'Initiated'), (2, 'Success'), (3, 'Failed'), (4, 'Input url process failed')], default=1)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extractedlead_created', to=settings.AUTH_USER_MODEL)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lead.lead')),
                ('modified_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extractedlead_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
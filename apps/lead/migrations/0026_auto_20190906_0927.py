# Generated by Django 2.1.10 on 2019-09-06 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_remove_organization_donor'),
        ('lead', '0025_auto_20190906_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='author',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads_by_author', to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='lead',
            name='source',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads_by_source', to='organization.Organization'),
        ),
    ]

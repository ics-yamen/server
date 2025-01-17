# Generated by Django 2.1.10 on 2019-09-12 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_remove_organization_donor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'permissions': (('can_merge', 'Can Merge organizations'),)},
        ),
        migrations.AddField(
            model_name='organization',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='Deep will use the parent organization data instead of current', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_childs', to='organization.Organization'),
        ),
    ]

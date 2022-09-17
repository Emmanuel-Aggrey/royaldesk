# Generated by Django 4.0 on 2022-07-28 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0010_rename_is_header_employee_is_head'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designation',
            name='reports_to',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_head': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_to', to='hrms.employee'),
        ),
    ]
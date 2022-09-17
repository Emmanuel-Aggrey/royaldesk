# Generated by Django 4.0 on 2022-07-28 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0006_alter_employee_employee_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='designation',
            name='net_month_salary',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='designation',
            name='provedent_amont',
            field=models.PositiveIntegerField(blank=True, help_text='value in percentage eg 5%', null=True),
        ),
        migrations.AddField(
            model_name='designation',
            name='provedent_amont_company',
            field=models.PositiveIntegerField(blank=True, help_text='value in percentage eg 5%', null=True),
        ),
        migrations.AddField(
            model_name='designation',
            name='reports_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_to', to='hrms.employee'),
        ),
        migrations.AddField(
            model_name='designation',
            name='snnit_amount',
            field=models.PositiveIntegerField(blank=True, help_text='value in percentage eg 5.5%', null=True),
        ),
        migrations.AddField(
            model_name='designation',
            name='snnit_amount_company',
            field=models.PositiveIntegerField(blank=True, help_text='value in percentage eg 13%', null=True),
        ),
    ]
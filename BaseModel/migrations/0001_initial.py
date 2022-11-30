# Generated by Django 4.0.7 on 2022-11-30 01:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=70)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('shortname', models.CharField(blank=True, max_length=5, null=True)),
                ('for_management', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=70)),
                ('net_month_salary', models.PositiveIntegerField(blank=True, null=True)),
                ('snnit_amount', models.DecimalField(blank=True, decimal_places=2, default=5.5, help_text='value in percentage eg 5.5%', max_digits=5, null=True)),
                ('snnit_amount_company', models.DecimalField(blank=True, decimal_places=2, default=13, help_text='value in percentage eg 13%', max_digits=5, null=True)),
                ('provedent_amont', models.DecimalField(blank=True, decimal_places=2, default=5, help_text='value in percentage eg 5%', max_digits=5, null=True)),
                ('provedent_amont_company', models.DecimalField(blank=True, decimal_places=2, default=5, help_text='value in percentage eg 5%', max_digits=5, null=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='BaseModel.department')),
                ('report_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_to', to='BaseModel.designation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

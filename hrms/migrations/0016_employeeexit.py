# Generated by Django 4.0.7 on 2023-01-09 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0015_alter_employee_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeExit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.JSONField(blank=True, default=dict, null=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_exit', to='hrms.employee')),
            ],
            options={
                'verbose_name': 'Employee Edit Form',
                'verbose_name_plural': 'Employee Edit Form',
            },
        ),
    ]

# Generated by Django 4.0 on 2022-08-10 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0020_alter_employee_applicant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='staff',
        ),
        migrations.DeleteModel(
            name='Recruitment',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]
# Generated by Django 4.0.7 on 2022-12-16 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0005_alter_employee_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='leave',
            unique_together=set(),
        ),
    ]
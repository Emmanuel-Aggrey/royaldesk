# Generated by Django 4.0.7 on 2022-11-01 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0045_remove_leave_reason_leave_resuming_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='handle_over_to',
        ),
    ]

# Generated by Django 4.0.7 on 2022-11-18 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0065_alter_leavepolicy_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='age',
        ),
        migrations.AddField(
            model_name='employee',
            name='exit_status',
            field=models.CharField(blank=True, choices=[('active', 'ACTIVE'), ('sacked', 'SACKED'), ('resign', 'RESIGN')], max_length=10, null=True),
        ),
    ]

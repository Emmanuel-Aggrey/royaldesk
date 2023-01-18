# Generated by Django 4.0.7 on 2022-09-10 07:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0022_alter_employee_request_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestchange',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requestchange',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

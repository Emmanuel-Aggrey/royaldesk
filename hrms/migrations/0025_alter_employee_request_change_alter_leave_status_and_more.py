# Generated by Django 4.0.7 on 2022-09-11 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0024_alter_employee_request_change'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='request_change',
            field=models.BooleanField(default=False, help_text='requested for data changes', null=True),
        ),
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(choices=[('approved', 'APPROVED'), ('unapproved', 'UNAPPROVED'), ('pending', 'PENDING'), ('done', 'DONE')], default='pending', max_length=15),
        ),
        migrations.AlterField(
            model_name='requestchange',
            name='status',
            field=models.CharField(choices=[('approved', 'APPROVED'), ('unapproved', 'UNAPPROVED'), ('pending', 'PENDING'), ('done', 'DONE')], default='pending', max_length=20),
        ),
    ]

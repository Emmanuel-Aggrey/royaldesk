# Generated by Django 4.0.7 on 2022-12-20 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_applicant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_normal_user',
            field=models.BooleanField(default=False),
        ),
    ]
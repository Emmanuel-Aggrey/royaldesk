# Generated by Django 4.0.7 on 2022-12-21 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='comment',
        ),
    ]
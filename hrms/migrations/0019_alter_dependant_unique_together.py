# Generated by Django 4.0 on 2022-08-03 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0018_alter_education_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dependant',
            unique_together={('first_name', 'last_name', 'address')},
        ),
    ]

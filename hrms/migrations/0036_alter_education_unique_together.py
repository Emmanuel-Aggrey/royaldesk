# Generated by Django 4.0.7 on 2022-09-17 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0035_alter_previouseployment_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='education',
            unique_together={('school_name', 'course', 'employee')},
        ),
    ]
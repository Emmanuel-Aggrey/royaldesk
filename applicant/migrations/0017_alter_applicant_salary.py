# Generated by Django 4.0 on 2022-08-10 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0016_rename_sala_applicant_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='salary',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

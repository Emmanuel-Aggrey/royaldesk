# Generated by Django 4.0.7 on 2022-12-21 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0002_remove_applicant_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='cv/%Y-%m-%d'),
        ),
    ]

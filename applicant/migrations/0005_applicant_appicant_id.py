# Generated by Django 4.0 on 2022-07-24 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0004_alter_applicant_designation'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='appicant_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]

# Generated by Django 4.0.7 on 2022-11-30 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='designation',
            options={'ordering': ['department', 'name']},
        ),
    ]
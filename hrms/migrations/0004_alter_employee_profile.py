# Generated by Django 4.0.7 on 2022-12-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0003_alter_leave_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='employees/%Y-%m-%d'),
        ),
    ]
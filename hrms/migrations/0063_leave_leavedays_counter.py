# Generated by Django 4.0.7 on 2022-11-14 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0062_remove_leave_leavedays_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='leavedays_counter',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
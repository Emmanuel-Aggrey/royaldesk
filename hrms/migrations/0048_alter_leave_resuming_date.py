# Generated by Django 4.0.7 on 2022-11-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0047_remove_leave_collegue_approve_leave_supervisor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='resuming_date',
            field=models.DateField(null=True),
        ),
    ]

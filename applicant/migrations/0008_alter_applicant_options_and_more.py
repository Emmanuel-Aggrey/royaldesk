# Generated by Django 4.0.7 on 2022-12-25 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0007_alter_offerletter_options_applicant_is_appicant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicant',
            options={'ordering': ('-updated_at',)},
        ),
        migrations.RenameField(
            model_name='applicant',
            old_name='is_appicant',
            new_name='is_applicant',
        ),
    ]

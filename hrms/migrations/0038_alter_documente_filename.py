# Generated by Django 4.0.7 on 2022-10-12 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0037_file_documente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documente',
            name='filename',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='filenames', to='hrms.file'),
        ),
    ]
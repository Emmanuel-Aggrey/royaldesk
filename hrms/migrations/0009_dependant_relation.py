# Generated by Django 4.0.7 on 2022-12-19 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0008_professionalmembership_document_alter_documente_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependant',
            name='relation',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

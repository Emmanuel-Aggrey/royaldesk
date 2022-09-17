# Generated by Django 4.0 on 2022-07-24 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0006_alter_employee_employee_id'),
        ('applicant', '0003_alter_applicant_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='designation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_designation', to='hrms.designation'),
        ),
    ]
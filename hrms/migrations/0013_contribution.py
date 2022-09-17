# Generated by Django 4.0 on 2022-07-31 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrms', '0012_remove_department_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('snnit_amount', models.DecimalField(blank=True, decimal_places=2, default=5.5, help_text='value in percentage eg 5.5%', max_digits=5, null=True)),
                ('snnit_amount_company', models.DecimalField(blank=True, decimal_places=2, default=13, help_text='value in percentage eg 13%', max_digits=5, null=True)),
                ('provedent_amont', models.DecimalField(blank=True, decimal_places=2, default=5, help_text='value in percentage eg 5%', max_digits=5, null=True)),
                ('provedent_amont_company', models.DecimalField(blank=True, decimal_places=2, default=5, help_text='value in percentage eg 5%', max_digits=5, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
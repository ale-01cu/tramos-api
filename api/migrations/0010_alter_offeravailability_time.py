# Generated by Django 5.2.4 on 2025-07-13 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_time_str_offeravailability_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offeravailability',
            name='time',
            field=models.TimeField(),
        ),
    ]

# Generated by Django 5.2.4 on 2025-07-12 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_offeravailability_time_str'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offeravailability',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]

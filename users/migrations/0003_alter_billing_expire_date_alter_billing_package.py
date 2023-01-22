# Generated by Django 4.1.5 on 2023-01-21 18:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_billing_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='expire_date',
            field=models.DateTimeField(default=datetime.date(2023, 1, 24)),
        ),
        migrations.AlterField(
            model_name='billing',
            name='package',
            field=models.CharField(choices=[('0', 'Testing Package'), ('500', 'Basic'), ('1000', 'Premium'), ('1500', 'Gold Package')], max_length=25),
        ),
    ]

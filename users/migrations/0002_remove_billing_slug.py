# Generated by Django 4.1.5 on 2023-01-19 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billing',
            name='slug',
        ),
    ]

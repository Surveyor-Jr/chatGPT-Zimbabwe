# Generated by Django 4.1.5 on 2023-01-19 20:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('coupon_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('discount_percentage', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'Coupons',
            },
        ),
        migrations.CreateModel(
            name='PackageList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('price_rtgs', models.FloatField()),
                ('duration_days', models.IntegerField()),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Subscription Packages',
            },
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(help_text='Mobile Number - (e.g. 0776887606', max_length=10)),
                ('paid_on', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField()),
                ('payment_method', models.CharField(choices=[('ecocash', 'Ecocash'), ('onemoney', 'OneMoney')], max_length=10)),
                ('expire_date', models.DateTimeField(default=datetime.date(2023, 1, 22))),
                ('reference_code', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('poll_url', models.TextField(null=True)),
                ('payment_status', models.TextField(null=True)),
                ('slug', models.SlugField(null=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.packagelist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bill Payments',
            },
        ),
    ]

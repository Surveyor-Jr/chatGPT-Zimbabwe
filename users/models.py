from datetime import timedelta, date
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save

import uuid

from django.utils import timezone

from users.tokens import account_activation_token


def activate_user(sender, instance, created, **kwargs):
    if created or (not instance.is_active):
        instance.is_active = True
        instance.save()


post_save.connect(activate_user, sender=User)

PAYMENT_METHOD = (
    ('ecocash', 'Ecocash'),
    ('onemoney', 'OneMoney'),
)

SUBSCRIPTION_PACKAGE = (
    ('1', 'Testing Package'),
    ('500', 'Basic (valid for 24hrs)'),
)


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    expiry_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.token = account_activation_token.make_token(self.user)
        self.expiry_date = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10, primary_key=True)
    description = models.TextField()
    discount_percentage = models.FloatField()

    def __str__(self):
        return self.coupon_code

    class Meta:
        verbose_name_plural = 'Coupons'


class PackageList(models.Model):
    name = models.CharField(max_length=250)
    price_rtgs = models.FloatField()
    duration_days = models.IntegerField()
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Subscription Packages'

    def __str__(self):
        return '{} - RTGS {} - {} days'.format(self.name, self.price_rtgs, self.duration_days)


class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    package = models.CharField(choices=SUBSCRIPTION_PACKAGE, max_length=25)
    phone = models.CharField(max_length=10, help_text='Mobile Number - (e.g. 0776887606')
    paid_on = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD)
    expire_date = models.DateTimeField(default=date.today() + timedelta(hours=24))
    reference_code = models.UUIDField(default=uuid.uuid4, editable=False)
    # PayNow Variables
    poll_url = models.TextField(null=True)
    payment_status = models.TextField(null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Bill Payments'

    def get_absolute_url(self):
        return reverse('invoice', kwargs={'reference_code': self.reference_code})

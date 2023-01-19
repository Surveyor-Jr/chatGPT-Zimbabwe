from datetime import timedelta, date
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import uuid


PAYMENT_METHOD = (
    ('ecocash', 'Ecocash'),
    ('onemoney', 'OneMoney'),
)


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
        return self.name


class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=10, help_text='Mobile Number - (e.g. 0776887606')
    paid_on = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD)
    expire_date = models.DateTimeField(default=date.today() + timedelta(days=3))
    reference_code = models.UUIDField(default=uuid.uuid4, editable=False)
    # PayNow Variables
    poll_url = models.TextField(null=True)
    payment_status = models.TextField(null=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Bill Payments'


    # def get_absolute_url(self):
    #     return reverse('invoice_detail', kwargs={"slug": self.slug})

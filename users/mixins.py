from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from users.models import Billing


def subscription_check(user):
    """
    Checks to see if a user's subscription for the service is still active.
    If not, the user cannot access the service page
    :param user:
    :return: True or False
    """
    try:
        subscription = Billing.objects.filter(user=user).latest('expire_date')
    except Billing.DoesNotExist:
        return False
    if subscription.expire_date < timezone.now():
        return False
    return True


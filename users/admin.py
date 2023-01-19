from django.contrib import admin
from .models import Billing, Coupon


class BillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'paid_on', 'amount', 'expire_date')
    list_filter = ('user',)


class CouponAdmin(admin.ModelAdmin):
    pass


admin.site.register(Billing, BillingAdmin)
admin.site.register(Coupon, CouponAdmin)

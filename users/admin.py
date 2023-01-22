from django.contrib import admin
from .models import Billing, Coupon, PackageList, Token


class BillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'paid_on', 'amount', 'expire_date')
    list_filter = ('user',)


class CouponAdmin(admin.ModelAdmin):
    pass


class PackageListAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_rtgs', 'duration_days', 'description')


class TokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Billing, BillingAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(PackageList, PackageListAdmin)
admin.site.register(Token, TokenAdmin)

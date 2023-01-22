from django.urls import path
from users import views as user_views
from .views import Invoice


urlpatterns = [
    path('', user_views.profile_menu, name='profile_menu'),
    path('billing_and_invoice', user_views.billing_and_invoice, name='billing_and_invoice'),
    path('invoice/<str:reference_code>/', Invoice.as_view(), name='invoice'),
    # path('expired_subscription/', )
]
from django.urls import path
from users import views as user_views


urlpatterns = [
    path('', user_views.profile_menu, name='profile_menu'),
    path('billing_and_invoice', user_views.billing_and_invoice, name='billing_and_invoice'),
]
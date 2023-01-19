from django.shortcuts import render


def profile_menu(request):
    return render(request, 'users/profile_menu.html')


def billing_and_invoice(request):
    return render(request, 'users/billing_and_invoice.html')

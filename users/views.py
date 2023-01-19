from django.shortcuts import render
from .form import BillingForm


def profile_menu(request):
    return render(request, 'users/profile_menu.html')


def billing_and_invoice(request):
    form = BillingForm

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            pass

    context = {'form': form}
    return render(request, 'users/billing_and_invoice.html', context)

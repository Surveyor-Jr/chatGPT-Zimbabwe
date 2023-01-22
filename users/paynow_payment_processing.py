from .form import BillingForm
from django.shortcuts import render, redirect
from django.contrib import messages
from chat_gptZimbabwe.settings import paynow
from django.conf import settings
from django.contrib.auth.models import User
from paynow import Paynow
import time


def processing_payment(request, form):
    phone_number = form.cleaned_data['phone']
    package_selected = form.cleaned_data['package']
    payment_method = form.cleaned_data['payment_method']
    email = 'matingonk@gmail.com'

    payment = paynow.create_payment('Order #100', email)
    payment.add('Zim-ChatGPT', package_selected)
    # Save PayNow Response
    response = paynow.send_mobile(payment, phone_number, payment_method)

    if response.success:
        # Save this to DB
        poll_url = response.poll_url
        # Payment Status
        # instructions = response.instructions #TODO: What does this really do?

        # Give time for user to pay
        time.sleep(30)

        # Check status of transaction
        status = paynow.check_transaction_status(poll_url)

        if status.paid:
            # Save the data to the DB
            instance = form.save(commit=False)
            instance.user = request.user  # attach user profile
            instance.email = email
            instance.phone = phone_number
            instance.amount = package_selected
            instance.poll_url = poll_url  # PayNow variable
            instance.payment_status = status.status  # Paynow Variable
            instance.payment_method = payment_method
            instance.save()

            # TODO:-> Consider Sending Email Receipt to the user?
            # Give the user a response
            messages.success(request, f"Payment Status: {status.status}")
            return render(request, 'users/billing_and_invoice.html')

        else:
            messages.warning(request, f"The payment transaction failed with payment status: {status.status}. ")

    else:
        messages.warning(request, "An error occurred while trying to process the transactions. Please try again later")
    return redirect('billing_and_invoice')

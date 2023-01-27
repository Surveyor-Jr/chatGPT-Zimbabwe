from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .form import BillingForm, EmailUserCreationForm, MySetPasswordForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from .models import Billing, Token
from django.utils import timezone
from .paynow_payment_processing import processing_payment


def register(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!')
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            # user.username = form.cleaned_data.get('first_name') + form.cleaned_data.get('last_name')
            user.save()
            token = Token.objects.create(user=user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('users/email_templates/acc_active_email.html', {
                'user': user,
                # 'username': user.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'current_site': current_site,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            try:
                email.send()
                return redirect('account_activation_sent')
            except:
                return render(request, 'error_page.html',
                              {'error_message': 'An account was created but the email activation link was not sent to '
                                                'the specified email address. Please contact the administrator'})

    else:
        form = EmailUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        uid = int(uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(e)
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        form = MySetPasswordForm(user=user)
        if request.method == 'POST':
            form = MySetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                login(request, user)
                return redirect('login')
        return render(request, 'users/activate.html', {'form': form})
    else:
        print(f'Token: {token}, User: {user}')
        return render(request, 'users/account_activation_invalid.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Retrieve the user from the form's cleaned data
            user = form.get_user()
            # Log the user in
            login(request, user)
            return redirect('profile_menu')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required()
def profile_menu(request):
    return render(request, 'users/profile_menu.html')


@login_required()
def billing_and_invoice(request):
    user = request.user
    form = BillingForm
    today = timezone.now()
    try:
        billing_records = Billing.objects.filter(user=user)  # display all by user
        last_records = Billing.objects.filter(user=user).latest('paid_on')  # just the latest by user
    except Billing.DoesNotExist:
        last_records = {}
        billing_records = {}

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            processing_payment(request, form)

    else:
        form = BillingForm()

    context = {
        'form': form,
        'billing_records': billing_records,
        'last_records': last_records,
        'today': today,
    }
    return render(request, 'users/billing_and_invoice.html', context)


class Invoice(LoginRequiredMixin, DetailView):
    model = Billing
    template_name = 'users/invoice.html'
    pk_url_kwarg = 'reference_code'
    context_object_name = 'invoice_detail'

    def get_object(self, queryset=None):
        reference_code = self.kwargs.get(self.pk_url_kwarg)
        return self.model.objects.get(reference_code=reference_code)


def logout_view(request):
    logout(request)
    return redirect('landing_page')
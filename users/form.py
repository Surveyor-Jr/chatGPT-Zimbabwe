from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import forms, ModelForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from .models import Billing, Token
from django.core.exceptions import ValidationError


class EmailUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        exclude = ('password1', 'password2')

    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['first_name'].lower() + self.cleaned_data['last_name'].lower()
        i = 0
        while User.objects.filter(username=user.username).exists():
            i += 1
            user.username = self.cleaned_data['first_name'].lower() + self.cleaned_data['last_name'].lower() + str(i)
        if commit:
            user.save()
            Token.objects.create(user=user)
        return user


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm New Password'}))


class BillingForm(ModelForm):
    class Meta:
        model = Billing
        fields = ('package', 'phone', 'payment_method')
        widgets = {'package': forms.Select(attrs={'class': 'form-select', }),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select', })}

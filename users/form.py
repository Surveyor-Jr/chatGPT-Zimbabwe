from django.forms import forms, ModelForm
from django import forms
from .models import Billing


class  BillingForm(ModelForm):
    class Meta:
        model = Billing
        fields = ('package', 'phone', 'payment_method')
        widgets = {
            'package': forms.Select(attrs={
                'class': 'form-select',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select',
            })
        }
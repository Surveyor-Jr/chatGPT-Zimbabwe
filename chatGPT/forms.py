from django.forms import forms, ModelForm
from django import forms
from .models import UserPrompts


class PromptForm(ModelForm):
    user_request = forms.CharField(widget=forms.Textarea(attrs=
                                                         {
                                                             'id': 'user_request',
                                                             'class': 'form-control mb-3'
                                                         }
    ))

    class Meta:
        model = UserPrompts
        fields = ('user_request',)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .forms import PromptForm
from django.contrib.auth.decorators import user_passes_test
from users.mixins import subscription_check
import openai


def home_page(request):
    return render(request, 'chatGPT/landing_page.html')


@login_required()
def chatgpt_prompts(request):
    if not subscription_check(request.user):
        return render(request, 'error_page.html', {'error_message': 'Your subscription has expired. Purchase another '
                                                                    'subscription to continue using ZimChatGPT '
                                                                    'service'})
    form = PromptForm()
    output = None

    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            user_input_text = form.cleaned_data['user_request']
            # Get User IP Address
            user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            # Operation Starts Here
            # OpenAI API Key
            openai.api_key = "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"
            # Completions Work
            completions = openai.Completion.create(
                engine="text-davinci-002",
                prompt=user_input_text,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
            output = completions.choices[0].text

            # Save to Database
            instance = form.save(commit=False)
            instance.chatgpt_response = output
            instance.prompt_by = request.user
            # Get IP
            instance.user_ip = user_ip
            instance.save()

    context = {
        'form': form,
        'output': output,
    }
    return render(request, 'chatGPT/user_prompt.html', context)


def pricing(request):
    return render(request, 'chatGPT/pricing.html')


def about(request):
    return render(request, 'chatGPT/about.html')


def feature(request):
    return render(request, 'chatGPT/features.html')


def faq(request):
    return render(request, 'chatGPT/faq.html')


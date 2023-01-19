from django.urls import path
from chatGPT import views as user_prompt_views


urlpatterns = [
    path('', user_prompt_views.home_page, name='landing_page'),
    path('user_request/', user_prompt_views.chatgpt_prompts, name='user_prompts'),
    path('pricing/', user_prompt_views.pricing, name='pricing'),
]
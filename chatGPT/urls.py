from django.urls import path
from chatGPT import views as user_prompt_views
from chatGPT.views import UserPromptData


urlpatterns = [
    path('', user_prompt_views.home_page, name='landing_page'),
    path('user_request/', user_prompt_views.chatgpt_prompts, name='user_prompts'),
    # Data Dependant Views
    path('database/chatgpt/', UserPromptData.as_view(), name='user_prompts_data_list'),
    # Static Views
    path('pricing/', user_prompt_views.pricing, name='pricing'),
    path('about/', user_prompt_views.about, name='about'),
    path('features/', user_prompt_views.feature, name='features'),
    path('faq/', user_prompt_views.faq, name='faq'),
]
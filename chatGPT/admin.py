from django.contrib import admin
from .models import UserPrompts


class UserPromptsAdmin(admin.ModelAdmin):
    list_display = ('request_key', 'user_request', 'chatgpt_response')


admin.site.register(UserPrompts, UserPromptsAdmin)

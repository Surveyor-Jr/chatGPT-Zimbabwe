from django.db import models
from django.contrib.auth.models import User
import uuid


class UserPrompts(models.Model):
    request_key = models.UUIDField(default=uuid.uuid4, editable=False)
    user_request = models.TextField(help_text='Enter your request here', verbose_name='How can I help you?')
    chatgpt_response = models.TextField(null=True, blank=True)
    # Metadata
    prompt_by = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt_date_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User Chat Prompts'

    def __str__(self):
        return str(self.request_key)



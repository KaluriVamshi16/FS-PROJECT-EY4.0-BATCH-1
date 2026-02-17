from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    is_user_message = models.BooleanField(default=True) # True if user sent, False if bot sent
    timestamp = models.DateTimeField(auto_now_add=True)
    context_data = models.JSONField(null=True, blank=True) # Store context or action taken

    def __str__(self):
        sender = "User" if self.is_user_message else "Bot"
        return f"{sender} - {self.timestamp}"

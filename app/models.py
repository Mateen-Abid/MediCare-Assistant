from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Conversation(models.Model):
    """Represents a chat conversation between a user and the chatbot"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title or 'Untitled'} ({self.created_at.strftime('%Y-%m-%d')})"

    @property
    def last_message_preview(self):
        """Get a preview of the last message"""
        last_message = self.messages.last()
        if last_message:
            return last_message.content[:50] + "..." if len(last_message.content) > 50 else last_message.content
        return "No messages yet"


class Message(models.Model):
    """Represents a single message in a conversation"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."

from django.db import models
from django.core.exceptions import ValidationError


class UserProfileModel(models.Model):
    chat_id = models.BigIntegerField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=55, blank=True, null=True)
    username = models.CharField(max_length=55, blank=True, null=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ('chat_id',)

    def __str__(self):
        return f'{self.first_name} ({self.username})' if self.first_name else str(self.chat_id)


class MessageModel(models.Model):
    user = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(blank=False, null=False)
    telegram_message_id = models.BigIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['deleted', 'created_at']),
        ]

    def __str__(self):
        return f'Message {self.telegram_message_id} for {self.user}'

    def clean(self):
        if self.deleted and not self.deleted_at:
            raise ValidationError("Поле 'deleted_at' должно быть заполнено, если сообщение удалено.")
        if not self.deleted and self.deleted_at:
            raise ValidationError("Поле 'deleted_at' должно быть пустым, если сообщение не удалено.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

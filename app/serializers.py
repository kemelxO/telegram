from rest_framework import serializers
from .models import MessageModel

class MessageSerializer(serializers.ModelSerializer):
    user_chat_id = serializers.IntegerField(source='user.chat_id', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = MessageModel
        fields = (
            'id', 'user_chat_id', 'user_first_name', 'user_username', 'text',
            'telegram_message_id', 'created_at', 'deleted', 'deleted_at',
        )
        read_only_fields = (
            'id', 'user_chat_id', 'user_first_name', 'user_username',
            'telegram_message_id', 'created_at', 'deleted', 'deleted_at',
        )

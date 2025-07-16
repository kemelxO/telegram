from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfileModel, MessageModel
from .services.telegram_api import send_telegram_message, delete_telegram_message
from django.utils import timezone


class TelegramWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        message = data.get('message')
        text = message.get('text', '')
        chat = message.get('chat', {})
        chat_id = chat.get('id')

        if not chat_id:
            return Response({"error": "chat_id не найден"}, status=400)

        first_name = chat.get('first_name', '')
        username = chat.get('username', '')

        user, _ = UserProfileModel.objects.get_or_create(chat_id=chat_id)
        user.first_name = first_name
        user.username = username
        user.save()

        if text == '/start':
            return Response({"message": "Пользователь зарегистрирован"}, status=200)

        if text == '/message':
            msg_text = f'Это сообщение будет удалено через 5 минут для пользователя {first_name}'
            response = send_telegram_message(chat_id, msg_text)

            if not response.get('ok'):
                return Response({"error": response.get('description', 'Ошибка отправки')}, status=400)

            telegram_message_id = response['result']['message_id']

            MessageModel.objects.create(
                user=user,
                text=msg_text,
                telegram_message_id=telegram_message_id,
            )

            return Response({"message": "Сообщение отправлено и сохранено"}, status=201)

        if text == '/clear':
            five_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
            messages = MessageModel.objects.filter(
                user=user,
                deleted=False,
                created_at__lte=five_minutes_ago
            )

            for msg in messages:
                delete_telegram_message(chat_id, msg.telegram_message_id)
                msg.deleted = True
                msg.deleted_at = timezone.now()
                msg.save()

            return Response({"message": "Старые сообщения удалены"}, status=200)

        return Response({"message": "Неизвестная команда"}, status=200)

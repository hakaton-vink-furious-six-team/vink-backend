from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from apps.chat.models import Chat
from apps.chat.api_v1.serializers import ChatRatingSerializer


class ChatRatingViewSet(ViewSet):
    """
    ViewSet для обновления рейтинга чата.
    """

    def create(self, request):
        serializer = ChatRatingSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data["user_id"]
            rating = serializer.validated_data["rating"]
            try:
                chat = Chat.objects.get(user_id=user_id, is_open=True)
                chat.rating = rating
                chat.save()
                return Response(
                    {"detail": "Рейтинг обновлен"}, status=status.HTTP_200_OK
                )
            except Chat.DoesNotExist:
                return Response(
                    {"detail": "Чат не найден"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

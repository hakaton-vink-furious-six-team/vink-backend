from rest_framework import serializers
from apps.chat.models import Chat


class ChatRatingSerializer(serializers.Serializer):
    """Серализатор для добавления рейтинга к чату."""

    user_id = serializers.IntegerField()
    rating = serializers.ChoiceField(choices=Chat.RATING_CHOICES)

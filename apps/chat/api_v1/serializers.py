from rest_framework import serializers
from apps.chat.models import Chat


class ChatRatingSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    rating = serializers.ChoiceField(choices=Chat.RATING_CHOICES)

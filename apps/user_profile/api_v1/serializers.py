from rest_framework import serializers

from apps.user_profile.models import UserProfile
from apps.chat.models import Chat


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя."""

    chat_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ("id", "name", "phone_number", "company_name", "chat_name")

    def get_chat_name(self, obj):  # noqa
        return obj.id

    def create(self, validated_data):
        """
        Проверяем наличие пользователя в базе по имени и номеру телефона,
        если такого нет то создаем нового. Так же обновляем данные,
        добавляя название компании.
        """
        name = validated_data.get("name")
        phone_number = validated_data.get("phone_number")
        if "company_name" in validated_data:
            company_name = validated_data.get("company_name")
            user, created = UserProfile.objects.get_or_create(  # noqa
                name=name, phone_number=phone_number
            )
            user.company_name = company_name
            user.save()
            chat, created = Chat.objects.get_or_create(user=user, is_open=True)
            return user
        user, created = UserProfile.objects.get_or_create(
            **validated_data
        )  # noqa
        return user

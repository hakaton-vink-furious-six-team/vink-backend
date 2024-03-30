from rest_framework import serializers

from apps.user_profile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя."""

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "name",
            "phone_number",
            "company_name",
        )

    def create(self, validated_data):
        user = UserProfile.objects.get_or_create(**validated_data)  # noqa
        return user

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
        """
        Проверяем наличие пользователя в базе по имени и номеру телефона,
        если такого нет то создаем нового. Так же обновляем данные,
        добавляя название компании.
        """
        name = validated_data.get("name")
        phone_number = validated_data.get("phone_number")
        if "company_name" in validated_data:
            company_name = validated_data.get("company_name")
            user, created = UserProfile.objects.get_or_create(
                name=name, phone_number=phone_number
            )  # noqa
            user.company_name = company_name
            user.save()
            return user
        user, created = UserProfile.objects.get_or_create(
            **validated_data
        )  # noqa
        return user

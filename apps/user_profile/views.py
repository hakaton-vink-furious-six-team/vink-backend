from rest_framework import viewsets

from apps.user_profile.api_v1.serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """Отправка данных о пользователе."""

    serializer_class = UserProfileSerializer
    http_method_names = [
        "post",
    ]

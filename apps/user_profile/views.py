from rest_framework import viewsets

from apps.user_profile.api_v1.serializers import UserProfileSerializer
from apps.user_profile.models import UserProfile


class UserProfileViewSet(viewsets.ModelViewSet):
    """Отправка данных о пользователе."""

    queryset = UserProfile.objects.all()  # noqa
    serializer_class = UserProfileSerializer
    http_method_names = [
        "post",
    ]

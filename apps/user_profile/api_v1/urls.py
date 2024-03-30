from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.user_profile.views import UserProfileViewSet

users_router_v1 = DefaultRouter()
users_router_v1.register(
    r"users",
    UserProfileViewSet,
    basename="users_profile",
)

urlpatterns = [
    path("", include(users_router_v1.urls)),
]

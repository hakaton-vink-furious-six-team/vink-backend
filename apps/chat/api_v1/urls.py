from django.urls import include
from rest_framework.routers import DefaultRouter

from django.urls import path
from apps.chat.views import ChatRatingViewSet

rate_router_v1 = DefaultRouter()
rate_router_v1.register(
    r"chat_rate",
    ChatRatingViewSet,
    basename="chat_rate",
)

urlpatterns = [
    path("", include(rate_router_v1.urls)),
]

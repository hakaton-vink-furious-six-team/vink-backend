from django.urls import path
from drf_spectacular import views as specview


urlpatterns = [
    path('doc/', specview.SpectacularAPIView.as_view(), name='schema'),
    path(
        'swagger/',
        specview.SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger'
    ),
    path(
        'redoc/',
        specview.SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    )
]

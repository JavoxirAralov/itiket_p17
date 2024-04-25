from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.views import RegisterCreateAPIView, ConfirmEmailAPIView

# from apps.views import UserViewSet,
#
# router = DefaultRouter()
# router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(),name='token_refresh'),
    path('users/sign-up', RegisterCreateAPIView.as_view(), name='register'),
    path('confirm-email/<uuid:pk>', ConfirmEmailAPIView.as_view(), name='register')
]

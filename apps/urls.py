from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.views import EventsListAPIView, CityListAPIView, CountryViewSet, ConfirmEmailAPIView

from apps.views import RegisterCreateAPIView, VenueListAPIView, UserUpdateAPIView, \
    ChangePasswordView, RequestResetPasswordEmail, PasswordTokenCheckAPI, SetNewPasswordAPI, VenueDetailAPIView

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/sign-up', RegisterCreateAPIView.as_view(), name='register'),
    path('events', EventsListAPIView.as_view(), name='events'),
    path('cities', CityListAPIView.as_view(), name='city_list'),
    path('confirm-email/<uuid:pk>/', ConfirmEmailAPIView.as_view(), name='register'),
    path('venues/', VenueListAPIView.as_view(), name='venues'),
    path('venues/<str:slug>/', VenueDetailAPIView.as_view(), name='venue'),
    path('profile-update/', UserUpdateAPIView.as_view(), name='profile_update'),
    path('password/', ChangePasswordView.as_view(), name='change_password'),
    path('request-reset-email/', RequestResetPasswordEmail.as_view(), name='request_reset_email'),
    path('password-resent/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPI.as_view(), name='password_reset_complete')

]

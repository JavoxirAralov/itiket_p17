from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.views import RegisterCreateAPIView, ConfirmEmailAPIView, EventsListAPIView, CountryListAPIView, \
    CityListAPIView

from apps.views import RegisterCreateAPIView, ConfirmEmailAPIView, VenueListAPIView, UserUpdateAPIView, \
    ChangePasswordView, RequestResetPasswordEmail, PasswordTokenCheckAPI, SetNewPasswordAPI
from django.contrib.auth import views as auth_views
# from apps.views import UserViewSet,
#
# router = DefaultRouter()
# router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(),name='token_refresh'),
    path('users/sign-up', RegisterCreateAPIView.as_view(), name='register'),
    path('confirm-email/<uuid:pk>', ConfirmEmailAPIView.as_view(), name='register'),
    path('events', EventsListAPIView.as_view(), name='events'),
    path('countries', CountryListAPIView.as_view(), name='country_list'),
    path('cities', CityListAPIView.as_view(), name='city_list'),
    path('users/sign-up/', RegisterCreateAPIView.as_view(), name='register'),
    path('confirm-email/<uuid:pk>/', ConfirmEmailAPIView.as_view(), name='register'),
    path('venues/', VenueListAPIView.as_view(), name='venues'),
    path('profile/', UserUpdateAPIView.as_view(), name='profile'),
    path('password/', ChangePasswordView.as_view(), name='change_password'),
    path('request-reset-email/', RequestResetPasswordEmail.as_view(), name='request_reset_email'),
    path('password-resent/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPI.as_view(), name='password_reset_complete')

]

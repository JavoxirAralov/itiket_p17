from rest_framework.viewsets import ModelViewSet

from apps.models import User, Event, Country, City, Promotion
from apps.serializers import CityModelSerializer, EventsModelSerializer, CountryModelSerializer, \
    PromotionModelSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.models import User, Venue
from apps.serializers import RegisterModelSerializer, VenueModelSerializer, UpdateUserModelSerializer, \
    ChangePasswordSerializer, ResetPasswordRequestSerializer, SetNewPasswordSerializer
from django.core.cache import cache
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.utils import send_verification_email
from django.utils.encoding import smart_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from apps.pagination import PageSortNumberPagination


class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer

    def get_success_headers(self, data):
        import uuid
        _uuid = uuid.uuid4()
        send_verification_email(data['email'], _uuid.__str__())
        cache.set(_uuid, data['email'])
        print('sent email!')
        return super().get_success_headers(data)


class ConfirmEmailAPIView(APIView):
    def get(self, request, pk):
        '''
                     ```User yaratilyatganda emaildan tasdiqlash```

        '''
        email = cache.get(pk)
        User.objects.filter(email=email).update(is_active=True)
        return Response({'message': 'User confirmed email!'})


class EventsListAPIView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsModelSerializer
    pagination_class = PageSortNumberPagination


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer


class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityModelSerializer


class VenueListAPIView(ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueModelSerializer
    pagination_class = PageSortNumberPagination


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserModelSerializer
    http_method_names = ['patch']

    def get_object(self):
        '''
                ```User malumotlarini  yangilish```

        '''
        return self.request.user

class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    http_method_names = ['patch']


    def get_object(self):
        return self.request.user


class RequestResetPasswordEmail(GenericAPIView):

    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        '''
        ```PASSWORD esdan chiqsa emailga passwordni yangilash uchun habar yuboradi```

        '''
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            aburl = 'http://' + current_site + relativeLink
            email_body = 'Hello,\n Use link below to reset your password: \n' + aburl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Password reset'}
            Util.send_email(data)
        return Response({'success': 'We have sent you link to reset your password!'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def get(self, request, uidb64, token):
        '''
               ```PASSWORD Resent qilish uchun Token Togri  ekanligini tekshirsh```

        '''

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid token or password'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPI(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        '''
                     ```Password esdan chiqanda yanglash```

        '''

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        return Response({'success': True, 'message': "Your password has been updated!"}, status=status.HTTP_200_OK)

class VenueDetailAPIView(ListAPIView):
    queryset = Venue.objects.order_by('slug')
    serializer_class = VenueModelSerializer
    pagination_class = None


class PromotionListAPIView(ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionModelSerializer
    pagination_class = None





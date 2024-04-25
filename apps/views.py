from apps.models import User
from apps.serializers import RegisterModelSerializer
from django.core.cache import cache
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.utils import send_verification_email


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
        email = cache.get(pk)
        User.objects.filter(email=email).update(is_active=True)
        return Response({'message': 'User confirmed email!'})

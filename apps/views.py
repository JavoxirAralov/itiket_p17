from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView
from apps.models import User
from apps.serializers import UserModelSerializer, UserCreateModelSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)
    search_fields = ('firstname', 'email')

    @action(detail=False, methods=['GET'], url_path='get-me')
    def get_me(self, request, pk=None):
        if request.user.is_authenticated:
            return Response({'message': f'{request.user.username}'})
        return Response({'message': 'login qilinmagan'})




class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateModelSerializer



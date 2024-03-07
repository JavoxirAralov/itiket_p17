from .models import User ,Event,Promotion,Location,Venue
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'password', 'date_joined', 'is_superuser')


class UserDetailModelSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('groups', 'user_permissions', 'password')


class UserCreateModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone','email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, password):
        return make_password(password)



# class EventModelSerializer(ModelSerializer):
#     class Meta:
#         model = Event
#         exclude= ("price")


from django.contrib.auth.password_validation import validate_password
from django.template.defaultfilters import default
from requests import request
from rest_framework.exceptions import AuthenticationFailed

from .models import User, Venue
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from rest_framework import serializers
from django.utils.encoding import smart_str, smart_bytes, force_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from .utils import Util


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
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, password):
        return make_password(password)


# class EventModelSerializer(ModelSerializer):
#     class Meta:
#         model = Event
#         exclude= ("price")
class VenueModelSerializer(ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class UpdateUserModelSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'birthday', 'city', 'gender',)
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False},
            'birthday': {'required': False},
            'city': {'required': False},
            'gender': {'required': False},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    # def update(self, instance, validated_data):
    #     instance.first_name = validated_data['first_name']
    #     instance.last_name = validated_data['last_name']
    #     instance.email = validated_data['email']
    #     instance.phone = validated_data['phone']
    #     instance.birthday = validated_data['birthday']
    #     instance.city = validated_data['city']
    #     instance.gender = validated_data['gender']
    #
    #     instance.save()
    #
    #     return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    class Meta:
        fields = ('email',)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(write_only=True, required=True)
    uidb64 = serializers.CharField(write_only=True, required=True)
    class Meta:
        fields = ('password', 'token', 'uidb64', 'password2')


    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            token = attrs.get('token')
            uid = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed({'message': 'Token expired'},)
            if attrs['password'] != attrs['password2']:
                 raise serializers.ValidationError({"password": "Password fields didn't match."})

            else:
                 user.set_password(password)
                 user.save()
        except Exception as e:
            raise AuthenticationFailed({'message': 'Token expired'}, )
        return super().validate(attrs)

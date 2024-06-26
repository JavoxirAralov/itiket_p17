from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.template.defaultfilters import default
from parler.forms import TranslatedField
from parler.models import TranslatableModel, TranslatedFields
from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer
from requests import request
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueTogetherValidator

from .models import User, Venue, Category, Promotion
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import ModelSerializer

from apps.models import User, Country, Event, City

from rest_framework import serializers
from django.utils.encoding import smart_str, smart_bytes, force_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from .utils import Util


class RegisterModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    email = EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('This email  was registered before')
        return value

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if confirm_password and confirm_password == data['password']:
            data['password'] = make_password(data['password'])
            data['is_active'] = False
            return data
        raise ValidationError("Parol mos emas")


class EventsModelSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Event)

    class Meta:
        model = Event
        fields = ['price', 'translations', 'city', 'slug', 'banner', 'venue', 'category', 'image_one', 'image_two']


class CountryModelSerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class UserCreateModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError({"email": "This email is already in use."})
        return value

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if confirm_password and confirm_password == data['password']:
            data['password'] = make_password(data['password'])
            data['is_active'] = False
            return data
        raise ValidationError({"passwor": "This password is not same "})

    def validate_password(self, password):
        return make_password(password)


class CityModelSerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


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
                raise AuthenticationFailed({'message': 'Token expired'}, )
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})

            else:
                user.set_password(password)
                user.save()
        except Exception as e:
            raise AuthenticationFailed({'message': 'Token expired'}, )
        return super().validate(attrs)



class EventSliderSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Event)

    class Meta:
        model = Event
        fields = ['price', 'translations', 'city', 'slug', 'banner', 'venue', 'category']


class EventOtherSerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=Event)

    class Meta:
        model = Event
        fields = ['price', 'translations', 'city', 'slug', 'venue', 'category', 'image_one', 'image_two']


class PromotionModelSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = ['id', 'name', 'events']  # Specify fields explicitly

    def to_representation(self, instance):

        if instance.name == 'Slider':
            return EventSliderSerializer(many=True).data
        else:
            return EventOtherSerializer(many=True).data





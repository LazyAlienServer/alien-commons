from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings

import string
import random
import io
from PIL import Image

from core.validators import (
    FileSizeValidator,
    FileTypeValidator,
    PasswordValidator,
    LengthValidator,
    RequiredValidator,
)


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'email', 'is_moderator', 'date_joined')
        read_only_fields = ('id', 'email', 'is_moderator', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="The email has already existed"),
            RequiredValidator,
        ],
    )
    password = serializers.CharField(write_only=True, validators=[PasswordValidator, RequiredValidator])
    confirm_password = serializers.CharField(write_only=True,validators=[RequiredValidator])

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        def pick_random_avatar():
            avatar = random.choice(settings.DEFAULT_AVATARS)
            return avatar

        def generate_unique_username():
            while True:
                uid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
                username = f"user_{uid}"
                if not User.objects.filter(username=username).exists():
                    return username

        user = User(
            email=validated_data['email'],
            username=generate_unique_username(),
            avatar=pick_random_avatar(),
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UsernameUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(queryset=User.objects.all(), message='The username has already existed',),
            LengthValidator(field_name='username', max_length=10)
        ]
    )

    class Meta:
        model = User
        fields = ('username',)


class AvatarUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(
        validators=[
            FileSizeValidator(object_display_name="avatar", max_size_mb=2),
            FileTypeValidator(object_display_name="avatar")
        ]
    )

    class Meta:
        model = User
        fields = ('avatar',)

    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar')

        image = Image.open(avatar)
        image = image.convert("RGB")
        image.thumbnail((512, 512))
        buffer = io.BytesIO()
        image.save(buffer, format="WEBP", quality=85)
        webp_file = ContentFile(buffer.getvalue())

        instance.avatar.save(f"{instance.pk}_avatar.webp", webp_file, save=False)
        instance.save()

        return instance


class CustomLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        access_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
        refresh_lifetime = api_settings.REFRESH_TOKEN_LIFETIME
        data['access_token_lifetime'] = str(access_lifetime.total_seconds())
        data['refresh_token_lifetime'] = str(refresh_lifetime.days)

        return data


class CustomLoginRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except ObjectDoesNotExist:
            raise AuthenticationFailed(
                self.error_messages.get("no_active_account", "No active account"),
                code="no_active_account",
            )

        access_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
        data["access_token_lifetime"] = str(access_lifetime.total_seconds())

        return data

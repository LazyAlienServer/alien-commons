from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from core.utils.file_types import FILE_TYPE_MAP


class LengthValidator:
    def __init__(self, field_name, max_length=10):
        self.field_name = field_name
        self.max_length = max_length

    def __call__(self, value):
        if len(value) > self.max_length:
            message = f"Your {self.field_name} must be less than {self.max_length} characters"
            raise serializers.ValidationError(message)


class PasswordValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def __call__(self, value):
        try:
            validate_password(value)
        except Exception:
            message = "Your password does not meet the requirement(s)"
            raise serializers.ValidationError(message)


class FileSizeValidator:
    def __init__(self, object_display_name, max_size_mb):
        self.object_name_display = object_display_name
        self.max_size_mb = max_size_mb * 1024 * 1024
        self.max_size_mb_display = max_size_mb

    def __call__(self, value):
        size = getattr(value, 'size', 0)

        if size > self.max_size_mb:
            message = f"Size of your {self.object_name_display} must be less than {self.max_size_mb_display} MB"
            raise serializers.ValidationError(message)


class FileTypeValidator:
    def __init__(self, object_display_name="file", allowed_types=None):
        self.object_name_display = object_display_name
        if allowed_types is None:
            allowed_types = ['image/jpeg', 'image/png', 'image/webp']
        self.allowed_types = allowed_types

    def __call__(self, value):
        content_type = getattr(value, 'content_type', None)

        if content_type not in self.allowed_types:

            allowed_types_display = [FILE_TYPE_MAP[mime_type, "Unknown Type"] for mime_type in self.allowed_types]
            message = f"Type of your {self.object_name_display} must be one of {allowed_types_display}"

            raise serializers.ValidationError(message)


class RequiredValidator:
    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, value):
        if value is None:
            message = f"Your {self.field_name} cannot be empty"

            raise serializers.ValidationError(message)

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from libs.open_api.serializers import OpenApiSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for creating users."""

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Return created user from validated data."""
        user = User(
            email=validated_data["email"],
            is_active=False  # Need email confirmation.
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Custom auth serializer to use email instead of username.
    Copied form rest_framework.authtoken.serializers.AuthTokenSerializer
    """
    email = serializers.CharField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password
        )

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict):
        """Escape warning."""

    def update(self, instance, validated_data):
        """Escape warning."""


class TokenSerializer(OpenApiSerializer):
    """Auth token for entire app."""
    expiry = serializers.IntegerField(
        help_text=f"Token expires in {settings.REST_KNOX['TOKEN_TTL']}"
    )
    token = serializers.CharField(help_text="Token itself")

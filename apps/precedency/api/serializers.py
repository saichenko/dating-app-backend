from rest_framework import serializers
from apps.precedency import models


class PrecedenceSerializer(serializers.ModelSerializer):
    """Serializer for Precedence model."""

    class Meta:
        model = models.Precedence
        fields = (
            "id",
            "title",
        )


class UsersPrecedencySerializer(serializers.ModelSerializer):
    """Serializer for UsersPrecedency with current user as default."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.UsersPrecedency
        fields = (
            "id",
            "precedency",
            "user",
            "attitude",
            "importance",
        )

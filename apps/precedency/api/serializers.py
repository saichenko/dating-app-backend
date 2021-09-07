from rest_framework import serializers
from apps.precedency import models


class PrecedenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Precedence
        fields = (
            "id",
            "title",
        )


class UsersPrecedencySerializer(serializers.ModelSerializer):

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

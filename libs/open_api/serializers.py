from rest_framework import serializers


class OpenApiSerializer(serializers.Serializer):
    """Serializer that should be used for customizing open_api spec.

    Made to avoid warnings about unimplemented methods

    """

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class DetailSerializer(OpenApiSerializer):
    """To show in spec responses like this {detail: text}."""
    detail = serializers.CharField(help_text="Message from backend")

from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from rest_framework import generics, permissions
from rest_framework.response import Response

from knox.views import LoginView as KnoxLoginView

from libs.notifications.email import DefaultEmailNotification

from .serializers import AuthTokenSerializer, RegisterSerializer


class RegisterAPIView(generics.GenericAPIView):
    """Create not active user which needs to be confirmed by email."""

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """Create not active user and send confirmation email."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        confirmation_lazy = reverse_lazy(
            "activate-account",
            kwargs={
                "uid64": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
        )
        confirmation_url = request.build_absolute_uri(confirmation_lazy)

        email_message = DefaultEmailNotification(
            subject=_("Account activation"),
            recipient_list=[user.email],
            template="users/emails/account_activation.html",
            confirmation_url=confirmation_url,
        )
        email_message.send()
        return Response({"status": "ok"}, status=200)


class LoginView(KnoxLoginView):
    """User authentication view.
    We"re using custom one because Knox using basic auth as default
    authorization method.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """Login user and get auth token with expiry."""
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request, serializer.validated_data["user"])
        return super().post(request, format=None)

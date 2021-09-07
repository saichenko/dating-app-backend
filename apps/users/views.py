from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from apps.users.models import User


@method_decorator(require_http_methods(["GET"]), name="dispatch")
class ActivateAccountView(TemplateView):
    """Activate account after email verification."""

    def get(self, request, *args, **kwargs):
        """Activate user if uid and token are valid."""
        uidb64 = self.kwargs.pop("uid64")
        token = self.kwargs.pop("token")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if not (user and default_token_generator.check_token(user, token)):
            return HttpResponse(_("Activation link is invalid!"), status=401)

        user.is_active = True
        user.save()
        return HttpResponse(status=200)

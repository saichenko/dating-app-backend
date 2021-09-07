from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.precedency import models
from .serializers import PrecedenceSerializer, UsersPrecedencySerializer


class PrecedenceViewSet(
        GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
):
    """ReadOnly ViewSet for precedency."""

    queryset = models.Precedence.objects.all()
    serializer_class = PrecedenceSerializer


class UsersPrecedencyViewSet(ModelViewSet):
    """CRUD ViewSet for current user UsersPrecedency objects."""

    queryset = models.UsersPrecedency.objects.all()
    serializer_class = UsersPrecedencySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return UsersPrecedency queryset related to current user."""
        return models.UsersPrecedency.objects.filter(user=self.request.user)

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from django_filters import rest_framework as filters

from apps.precedency import models
from apps.precedency.filters import PrecedenceFilter, UsersPrecedencyFilter

from .serializers import PrecedenceSerializer, UsersPrecedencySerializer


class PrecedenceViewSet(
        GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
):
    """ReadOnly ViewSet for precedency."""

    queryset = models.Precedence.objects.all()
    serializer_class = PrecedenceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PrecedenceFilter


class UsersPrecedencyViewSet(ModelViewSet):
    """CRUD ViewSet for current user UsersPrecedency objects."""

    queryset = models.UsersPrecedency.objects.all()
    serializer_class = UsersPrecedencySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UsersPrecedencyFilter

    def get_queryset(self):
        """Return UsersPrecedency queryset related to current user."""
        return models.UsersPrecedency.objects.filter(user=self.request.user)

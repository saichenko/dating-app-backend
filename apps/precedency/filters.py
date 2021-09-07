import django_filters

from .models import Precedence


class PrecedenceFilter(django_filters.FilterSet):
    """Precedence filterset class with icontains serch for title."""

    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Precedence
        fields = (
            "title",
        )

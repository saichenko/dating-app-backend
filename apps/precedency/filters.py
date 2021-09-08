import django_filters

from .models import Precedence, UsersPrecedency


class PrecedenceFilter(django_filters.FilterSet):
    """Precedence filterset class with icontains serch for title."""

    title = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Precedence
        fields = (
            "title",
        )


class UsersPrecedencyFilter(django_filters.FilterSet):
    """UsersPrecedency filterset class."""

    importance__gt = django_filters.NumberFilter(
        field_name="importance",
        lookup_expr="gt"
    )
    importance__lt = django_filters.NumberFilter(
        field_name="importance",
        lookup_expr="lt"
    )

    class Meta:
        model = UsersPrecedency
        fields = (
            "importance",
            "importance__gt",
            "importance__lt",
            "attitude",
            "precedency",
        )

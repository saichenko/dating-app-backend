import factory
from factory import fuzzy

from . import models


class PrecedenceFactory(factory.django.DjangoModelFactory):
    """Factory for generating Precedence instance."""

    title = factory.Faker("text")

    class Meta:
        model = models.Precedence


class UserPrecedencyFactory(factory.django.DjangoModelFactory):
    """Factory for generating UserPrecedency instance w/o user."""

    precedence = factory.SubFactory(PrecedenceFactory)
    attitude = fuzzy.FuzzyInteger(0, 1)
    importance = fuzzy.FuzzyInteger(1, 10)

    class Meta:
        model = models.UsersPrecedency

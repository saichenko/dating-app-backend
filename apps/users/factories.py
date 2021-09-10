import uuid

from django.contrib.auth import get_user_model

import factory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for generating test User instance."""

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True

    @factory.lazy_attribute
    def email(self):
        """Return formatted email.

        Use uuid instead of `Faker('email')` for avoiding collisions.
        """
        return f"{uuid.uuid4()}@example.com"

    class Meta:
        model = User

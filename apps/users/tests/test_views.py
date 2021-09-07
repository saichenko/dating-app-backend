from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest

from apps.users.factories import UserFactory

User = get_user_model()


@pytest.fixture(scope="function")
def inactive_user():
    """Function fixture for inactive users."""
    return UserFactory(is_active=False)


def test_activate_account_view(inactive_user, client, mocker):
    """Test ActivateAccountView activates user."""
    url = reverse("activate-account", kwargs={"token": "123", "uid64": "MQ"})
    # Replace getting user by its uid with `inactive_user` instance
    mocker.patch(
        "apps.users.models.User.objects.get",
        return_value=User.objects.get(id=inactive_user.id)
    )
    # Mocking token checking
    mocker.patch(
        "django.contrib.auth.tokens.default_token_generator.check_token",
        return_value=True
    )
    response = client.get(url)
    assert response.status_code == 200
    inactive_user.refresh_from_db()
    assert inactive_user.is_active

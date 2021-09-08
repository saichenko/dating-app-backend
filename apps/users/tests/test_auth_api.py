import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from knox.models import AuthToken

User = get_user_model()


@pytest.mark.parametrize("data", (
    ({"email": "paveldurov@tg.com", "password": "pasha123"}),
    ({"email": "mark@facebook.com", "password": "dadada"}),
    ({"email": "root@root.com", "password": "root"}),
    ({"email": "someemauk@gmail.com", "password": "i12mvz0d3f"}),
))
def test_user_registration_view(api_client, data):
    """Test RegisterAPIView creates not active users."""
    url = reverse("api:register")
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    user_instance = User.objects.get(email=data["email"])
    assert not user_instance.is_active  # Check user is not active.


def test_user_login_view(api_client, user):
    """Test LoginView return generated token."""
    url = reverse("api:login")
    tokens_before = AuthToken.objects.filter(user=user).count()
    data = {"email": user.email, "password": "123"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == 200
    assert response.data.get("token")
    assert tokens_before + 1 == AuthToken.objects.filter(user=user).count()


def test_user_logout_all_view(auth_api_client, user):
    """Test LogoutAllView deletes all user related tokens."""
    url = reverse("api:logoutall")
    response = auth_api_client.post(url)
    assert response.status_code == 204
    assert not AuthToken.objects.filter(user=user).exists()

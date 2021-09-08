import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.precedency.factories import PrecedenceFactory, UserPrecedencyFactory
from apps.precedency.models import UsersPrecedency

User = get_user_model()


@pytest.fixture(scope="function")
def precedence():
    """Function fixture for Precedence."""
    return PrecedenceFactory()


@pytest.fixture(scope="function")
def precedency():
    """Function fixture for 5 Precedency instances."""
    return PrecedenceFactory.create_batch(size=5)


@pytest.fixture(scope="function")
def users_precedency(user):
    """Function fixture for """
    return UserPrecedencyFactory(user=user)


def test_precedency_detail_view(api_client, precedence):
    """Test precedency detail view return correct instance."""
    url = reverse("api:precedency-detail", kwargs={"pk": precedence.pk})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["title"] == precedence.title


def test_precedency_list_view(api_client, precedency):
    """Test precedency list view return correct instances."""
    url = reverse("api:precedency-list")
    response = api_client.get(url)
    assert response.status_code == 200
    for precedence in precedency:
        obj = list(filter(
            lambda x: x['id'] == precedence.id,
            response.data)
        )[0]
        assert obj['title'] == precedence.title


@pytest.mark.parametrize("data", (
    ({"attitude": 1, "importance": 2}),
    ({"attitude": 0, "importance": 10}),
    ({"attitude": 0, "importance": 5}),
    ({"attitude": 1, "importance": 4}),
    ({"attitude": 1, "importance": 5}),
))
def test_users_precedency_action_create(auth_api_client, data, precedence):
    """Test users precedency creating action."""
    url = reverse("api:user-precedency-list")
    data["precedency"] = precedence.id
    response = auth_api_client.post(url, data, format="json")
    assert response.status_code == 201
    resp_data = response.data
    assert resp_data["attitude"] == data["attitude"]
    assert resp_data["importance"] == data["importance"]
    instance = UsersPrecedency.objects.get(pk=resp_data["id"])
    assert instance.user == response.wsgi_request.user


def test_users_precedency_delete_action(
    auth_api_client,
    user,
    users_precedency,
):
    """Test delete action for users precedency."""
    url = reverse(
        "api:user-precedency-detail",
        kwargs={"pk": users_precedency.pk}
    )
    response = auth_api_client.delete(url)
    assert response.status_code == 204
    assert not UsersPrecedency.objects.filter(pk=users_precedency.pk).exists()

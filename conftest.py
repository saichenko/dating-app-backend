"""Configuration file for pytest
"""

import pytest
from django.conf import settings
from rest_framework.test import APIClient

from apps.users.factories import UserFactory


def pytest_configure():
    """Set up Django settings for tests.

    `pytest` automatically calls this function once when tests are run.
    """
    settings.DEBUG = False
    settings.TESTING = True

    # The default password hasher is rather slow by design.
    # https://docs.djangoproject.com/en/3.0/topics/testing/overview/
    settings.PASSWORD_HASHERS = (
        "django.contrib.auth.hashers.MD5PasswordHasher",
    )
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # To disable celery in tests
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """This hook allows all tests to access DB"""


@pytest.fixture(scope="session", autouse=True)
def temp_directory_for_media(tmpdir_factory):
    """Fixture that set temp directory for all media files.

    This fixture changes FILE_STORAGE to filesystem and provides temp dir for
    media. PyTest cleans up this temp dir by itself after few test runs
    """
    settings.DEFAULT_FILE_STORAGE = (
        "django.core.files.storage.FileSystemStorage"
    )
    media = tmpdir_factory.mktemp("tmp_media")
    settings.MEDIA_ROOT = media


@pytest.fixture(scope="session")
def api_client():
    """Session fixture for APIClient."""
    return APIClient()


@pytest.fixture(scope="function")
def auth_api_client(user, api_client):
    """Function fixture for authenticated APIClient instance."""
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture(scope="function")
def user():
    """Function fixture for active user instances with password `123`."""
    instance = UserFactory.build()
    instance.set_password("123")
    instance.save()
    return instance

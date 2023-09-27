import pytest
from django.contrib.auth import get_user_model
import pytest
from rest_framework.test import APIClient
from users.models import CustomUser

User = get_user_model()


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        email="test@test.com",
        password="Password123!",
        surname="Tester",
        other_names="Resilient",
        date_of_birth="1990-01-24",
    )
    return user


@pytest.fixture
def api_client(test_user):
    client = APIClient()
    client.force_authenticate(test_user)
    return client


@pytest.fixture
def test_create_user(db, test_user):
    test_user, _ = CustomUser.objects.get_or_create(
        email="dexter400@gmail.com",
        other_names="Dexter",
        surname="Daniel",
        date_of_birth="2005-01-24",
        password="Simplepass123!",
    )
    return test_user

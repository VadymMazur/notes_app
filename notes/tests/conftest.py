import pytest

from .factories import CategoryFactory, NoteFactory, UserFactory


@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def note(user, category):
    return NoteFactory(user=user, category=category)


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client

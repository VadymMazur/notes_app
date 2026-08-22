from datetime import date, timedelta

import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from ..models import Category, Note


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda number: f'user{number}')
    password = factory.LazyFunction(lambda: make_password('password123'))


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker('word')


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    title = factory.Faker('sentence', nb_words=4)
    text = factory.Faker('sentence')
    reminder = factory.LazyFunction(lambda: date.today() + timedelta(days=1))
    category = factory.SubFactory(CategoryFactory)
    user = factory.SubFactory(UserFactory)

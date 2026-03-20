from datetime import date

import factory

from infrastructure.models import Assignment, Indicator, User, WellnessEntry


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user-{n}")
    email = factory.Sequence(lambda n: f"user-{n}@zenlog.test")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    role = User.Role.PATIENT


class CoachFactory(UserFactory):
    username = factory.Sequence(lambda n: f"coach-{n}")
    email = factory.Sequence(lambda n: f"coach-{n}@zenlog.test")
    role = User.Role.COACH


class AdminFactory(UserFactory):
    username = factory.Sequence(lambda n: f"admin-{n}")
    email = factory.Sequence(lambda n: f"admin-{n}@zenlog.test")
    role = User.Role.ADMIN


class IndicatorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Indicator

    name = factory.Sequence(lambda n: f"indicator-{n}")
    unit = "/10"
    min_value = 1.0
    max_value = 10.0
    is_active = True


class WellnessEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WellnessEntry

    patient = factory.SubFactory(UserFactory)
    indicator = factory.SubFactory(IndicatorFactory)
    date = factory.LazyFunction(date.today)
    value = 7.0
    note = None


class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assignment

    coach = factory.SubFactory(CoachFactory)
    patient = factory.SubFactory(UserFactory)
    start_date = factory.LazyFunction(date.today)
    is_active = True

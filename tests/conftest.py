from pytest_factoryboy import register

from tests.factories import AdFactory, CategoryFactory, UserFactory

pytest_plugins = "tests.fixtures"


register(UserFactory)
register(CategoryFactory)
register(AdFactory)

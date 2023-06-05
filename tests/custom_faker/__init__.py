from faker import Faker

from tests.custom_faker.providers import PermissionProvider, UserProvider

faker = Faker()

faker.add_provider(PermissionProvider)
faker.add_provider(UserProvider)

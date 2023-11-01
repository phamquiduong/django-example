from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class GetUserInfoTestCase(TestCase):
    TEST_EMAIL = 'test@test.test'
    TEST_PASSWORD = 'Test123!@#'
    TEST_FULL_NAME = 'User Test'

    def setUp(self):
        self.user = User.objects.create_user(email=self.TEST_EMAIL, password=self.TEST_PASSWORD)  # type: ignore
        self.user.full_name = self.TEST_FULL_NAME
        self.user.save()

    def test_get_user_info(self):
        res = self.user.dict()

        self.assertTrue('id' in res)
        self.assertTrue(isinstance(res['id'], int))

        self.assertTrue('email' in res)
        self.assertEqual(res['email'], self.TEST_EMAIL)

        self.assertTrue('is_superuser' in res)
        self.assertIs(res['is_superuser'], False)

        self.assertTrue('is_active' in res)
        self.assertIs(res['is_active'], True)

        self.assertTrue('full_name' in res)
        self.assertIs(res['full_name'], self.TEST_FULL_NAME)

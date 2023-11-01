from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.authentication.services import register
from utils.api.exception import APIException

User = get_user_model()


class RegisterTestCase(TestCase):
    TEST_EMAIL = 'test@test.test'
    TEST_PASSWORD = 'Test123!@#'

    def setUp(self):
        User.objects.create_user(email='email_already_exist@test.test', password=self.TEST_PASSWORD)  # type: ignore

    def test_register_user_success(self):
        user = register(email=self.TEST_EMAIL, password=self.TEST_PASSWORD)

        self.assertTrue('id' in user)
        self.assertTrue(isinstance(user['id'], int))

        self.assertTrue('email' in user)
        self.assertEqual(user['email'], self.TEST_EMAIL)

        self.assertTrue('is_superuser' in user)
        self.assertIs(user['is_superuser'], False)

        self.assertTrue('is_active' in user)
        self.assertIs(user['is_active'], True)

        self.assertTrue('full_name' in user)
        self.assertIs(user['full_name'], None)

    def test_email_is_null(self):
        try:
            register(email=None, password=self.TEST_PASSWORD)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-001-100')
        else:
            self.fail()

    def test_email_is_empty(self):
        try:
            register(email='', password=self.TEST_PASSWORD)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-001-100')
        else:
            self.fail()

    def test_password_is_null(self):
        try:
            register(email=self.TEST_EMAIL, password=None)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-001-110')
        else:
            self.fail()

    def test_password_is_empty(self):
        try:
            register(email=self.TEST_EMAIL, password='')
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-001-110')
        else:
            self.fail()

    def test_password_is_not_valid(self):
        try:
            register(email=self.TEST_EMAIL, password='123')
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-001-111')
        else:
            self.fail()

    def test_user_already_registered(self):
        try:
            register(email='email_already_exist@test.test', password=self.TEST_PASSWORD)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-409-001-100')
        else:
            self.fail()

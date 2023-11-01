from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.authentication.services import login
from utils.api.exception import APIException

User = get_user_model()


class LoginTestCase(TestCase):
    TEST_EMAIL = 'test@test.test'
    TEST_PASSWORD = 'Test123!@#'

    def setUp(self):
        User.objects.create_user(email=self.TEST_EMAIL, password=self.TEST_PASSWORD)  # type: ignore

    def test_login_user_success(self):
        user = login(email=self.TEST_EMAIL, password=self.TEST_PASSWORD)
        self.assertTrue('access_token' in user)
        self.assertTrue('refresh_token' in user)

    def test_email_is_null(self):
        try:
            login(email=None, password=self.TEST_PASSWORD)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-002-101')
        else:
            self.fail()

    def test_email_is_empty(self):
        try:
            login(email='', password=self.TEST_PASSWORD)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-002-101')
        else:
            self.fail()

    def test_password_is_null(self):
        try:
            login(email=self.TEST_EMAIL, password=None)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-002-111')
        else:
            self.fail()

    def test_password_is_empty(self):
        try:
            login(email=self.TEST_EMAIL, password='')
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-002-111')
        else:
            self.fail()

    def test_user_does_not_exist(self):
        try:
            login(email='does_not_exist@test.test', password=self.TEST_PASSWORD)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-404-002-101')
        else:
            self.fail()

    def test_password_incorrect(self):
        try:
            login(email=self.TEST_EMAIL, password='password_incorrect')
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-401-002-111')
        else:
            self.fail()

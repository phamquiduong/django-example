from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.authentication.helpers.token import AccessTokenHelper, RefreshTokenHelper
from apps.authentication.services import refresh_token
from utils.api.exception import APIException

User = get_user_model()


class RefreshTokenTestCase(TestCase):
    TEST_EMAIL = 'test@test.test'
    TEST_PASSWORD = 'Test123!@#'

    def setUp(self):
        self.user = User.objects.create_user(email=self.TEST_EMAIL, password=self.TEST_PASSWORD)  # type: ignore
        self.refresh_token = RefreshTokenHelper().render(user_id=self.user.id)
        self.access_token = AccessTokenHelper().render(user_id=self.user.id)

    def test_refresh_token_success(self):
        res = refresh_token(token=self.refresh_token)

        self.assertTrue('access_token' in res)
        self.assertEqual(AccessTokenHelper().auth(token=res['access_token']), self.user.id)

        self.assertTrue('refresh_token' in res)
        self.assertEqual(RefreshTokenHelper().auth(token=res['refresh_token']), self.user.id)

    def test_token_is_none(self):
        try:
            refresh_token(token=None)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-003-100')
        else:
            self.fail()

    def test_token_is_empty(self):
        try:
            refresh_token(token='')
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-400-003-100')
        else:
            self.fail()

    def test_token_invalid(self):
        try:
            refresh_token(token='incorrect token')
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-401-003-010')
        else:
            self.fail()

    def test_token_type_incorrect(self):
        try:
            refresh_token(token=self.access_token)
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-401-003-011')
        else:
            self.fail()

    def test_user_not_found(self):
        try:
            refresh_token(token=RefreshTokenHelper().render(user_id=self.user.id+1))
        except APIException as exc:
            self.assertEqual(exc.get_error_code(), 'E-404-003-100')
        else:
            self.fail()

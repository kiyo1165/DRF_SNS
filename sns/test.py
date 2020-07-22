from django.test import TestCase
from sns.logic import mul
from django.contrib.auth import get_user_model


class TestTest(TestCase):
    def testmul(self):
        self.assertEqual(mul(2,3),6)

class UserCreateTests(TestCase):
    def test_createuser(self):
        email = 'dummy@gmail.com'
        password = 'dummy'

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
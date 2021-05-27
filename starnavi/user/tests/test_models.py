from django.test import TestCase
from django.core.exceptions import ValidationError
from user.models import User

class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        user = User.objects.create_user(
            email='foo@bar.com', 
            nickname = 'foo', 
            password='bar'
        )

        superuser = User.objects.create_superuser(
            email='foo1@bar.com', 
            nickname = 'foo1', 
            password='bar'
        )
    def test_create_user(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.email, 'foo@bar.com')
        self.assertEqual(user.nickname, 'foo')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='', 
                nickname = 'foo', 
                password='bar'
            )
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='', 
                nickname = '', 
                password='bar'
            )
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='foo@bar.com', 
                nickname = '', 
                password='bar'
            )

    def test_create_superuser(self):
        superuser = User.objects.get(id=2)
        self.assertEqual(superuser.email, 'foo1@bar.com')
        self.assertEqual(superuser.nickname, 'foo1')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(superuser.username)
        except AttributeError:
            pass
        with self.assertRaises(ValidationError):
            User.objects.create_superuser(
                email='foo1@bar.com', 
                nickname = 'foo1', 
                password='bar', 
                is_superuser=False
            )
    
    def test_user_email_label(self):
        user = User.objects.get(id=1)
        email = user._meta.get_field('email').verbose_name
        self.assertEqual(email, 'email')

    def test_user_nickname_label(self):
        user = User.objects.get(id=1)
        nickname = user._meta.get_field('nickname').verbose_name
        self.assertEqual(nickname, 'nickname')
    
    def test_user_email_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEqual(max_length, 100)

    def test_user_nickname_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('nickname').max_length
        self.assertEqual(max_length, 100)

    def test_user_email_unique(self):
        user = User.objects.get(id=1)
        unique = user._meta.get_field('email').unique
        self.assertTrue(unique)

    def test_user_nickname_unique(self):
        user = User.objects.get(id=1)
        unique = user._meta.get_field('nickname').unique
        self.assertTrue(unique)

    def test_user_object_name(self):
        user = User.objects.get(id=1)
        nickname = user.nickname
        self.assertEqual(nickname, str(user))

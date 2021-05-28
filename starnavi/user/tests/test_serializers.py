from django.test import TestCase
from django.core.exceptions import ValidationError
from user.serializers import UserSignUpSerializer

class UserSerializerTestCase(TestCase):
    maxDiff = None
    
    def setUp(self):
        
        self.data = {
            'email': 'foo@bar.com', 
            'nickname': 'foo', 
            'password1': 'bar123$%',
            'password2': 'bar123$%',
        }

        self.data_passw_mismatch = {
            'email': 'foo@bar.com', 
            'nickname': 'foo', 
            'password1': 'bar123$%',
            'password2': 'bar123$',
        }

        self.data_weak_passw = {
            'email': 'foo@bar.com', 
            'nickname': 'foo', 
            'password1': 'bar',
            'password2': 'bar',
        }

        self.data_invalid = {
            'email': 'foo', 
            'nickname': 'foo', 
            'password1': 'bar',
            'password2': 'bar',
        }

    def test_user_signup(self):
        user_signup = UserSignUpSerializer(data=self.data)
        self.assertTrue(user_signup.is_valid())
    
    def test_user_signup_invalid_data(self):
        user_signup = UserSignUpSerializer(data=self.data_invalid)
        self.assertFalse(user_signup.is_valid())

    def test_user_signup_create(self):
        user_signup = UserSignUpSerializer()
        user_signup.create(validated_data=self.data)

    def test_user_signup_create_passw_mismatch(self):
        user_signup = UserSignUpSerializer()
        with self.assertRaises(ValidationError):
            user_signup.create(validated_data=self.data_passw_mismatch)

    def test_user_signup_create_weak_passw(self):
        user_signup = UserSignUpSerializer()
        with self.assertRaises(ValidationError):
            user_signup.create(validated_data=self.data_weak_passw)

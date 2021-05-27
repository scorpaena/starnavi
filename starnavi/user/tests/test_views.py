from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from user.models import User


class UserTestCase(TestCase):
    maxDiff = None
    
    def setUp(self):
        self.client_user = APIClient()
        self.client_superuser = APIClient()
        self.client_anonymous = APIClient() #will not be logged in
        
        self.user = User.objects.create_user(
            email='foo@bar.com', 
            nickname = 'foo', 
            password='bar'
        )

        self.superuser = User.objects.create_superuser(
            email='foo1@bar.com', 
            nickname = 'foo1', 
            password='bar'
        )

        self.token = AccessToken.for_user(self.superuser)
        self.client_superuser.credentials(
            HTTP_AUTHORIZATION='Bearer ' + str(self.token)
        )

        self.payload = {
            'email': 'foo2@bar.com', 
            'nickname': 'foo2', 
            'password1': 'bar123$%',
            'password2': 'bar123$%',
        }

        self.payload_weak_passw = {
            'email': 'foo3@bar.com', 
            'nickname': 'foo3', 
            'password1': 'bar',
            'password2': 'bar',
        }

        self.payload_passw_mismatch = {
            'email': 'foo4@bar.com', 
            'nickname': 'foo4', 
            'password1': 'bar123$%',
            'password2': 'foo123$%',
        }


    def test_user_signup(self):
        request = self.client_anonymous.post('/user/signup/', data=self.payload)
        self.assertEqual(request.status_code, 201)

    def test_user_signup_weak_password(self):
        with self.assertRaises(ValidationError):
            request = self.client_anonymous.post(
                '/user/signup/', 
                data=self.payload_weak_passw
            )

    def test_user_signup_password_mismatch(self):
        with self.assertRaises(ValidationError):
            request = self.client_anonymous.post(
                '/user/signup/', 
                data=self.payload_passw_mismatch
            )

    def test_superuser_get_lastlogin(self):
        response = self.client_superuser.get('/user/lastlogin/',)
        self.assertEqual(response.status_code, 200)

    def test_user_get_lastlogin(self):
        response = self.client_user.get('/user/lastlogin/',)
        self.assertEqual(response.status_code, 401)

    def test_user_login(self):
        request = self.client_user.post('/user/login/',
            data = {'email': 'foo@bar.com', 'password': 'bar'}
        )
        self.assertEqual(request.status_code, 200)
    
    def test_user_login_wrong_passw(self):
        request = self.client_user.post('/user/login/',
            data = {'email': 'foo@bar.com', 'password': 'foo'}
        )
        self.assertEqual(request.status_code, 403)

    def test_user_login_wrong_email(self):
        request = self.client_user.post('/user/login/',
            data = {'email': 'foo@bar1.com', 'password': 'bar'}
        )
        self.assertEqual(request.status_code, 403)

    def test_user_logout(self):
        response = self.client_user.get('/user/logout/',)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'),'you are logged out')


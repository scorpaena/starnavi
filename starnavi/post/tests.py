from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from datetime import date, timedelta
from user.models import User
from .models import Post, PostLikes

today = date.today()
yesterday = today-timedelta(days=1)


class PostTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        self.client = APIClient()
        self.client_anonymous = APIClient() #will not be logged in
        
        self.user = User.objects.create_user(
            email='foo@bar.com', 
            nickname = 'foo', 
            password='bar'
        )
 
       
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        
        self.payload_post = {
            'title': 'foo',
            'content': 'bar',
            'date_posted': today,
            'author': self.user
        }
        self.post = Post.objects.create(**self.payload_post)


        self.payload_post_like = {
            'user': self.user,
            'post': self.post,
            'date_liked': today,
        }
        self.payload_like = {'like_unlike': 'like'}
        self.payload_unlike = {'like_unlike': 'unlike'}


    def test_post_create(self):
        request = self.client.post('/post/', data=self.payload_post)
        self.assertEqual(request.status_code, 201)

    def test_post_create_anonymous(self):
        request = self.client_anonymous.post('/post/', data=self.payload_post)
        self.assertEqual(request.status_code, 401)

    def test_post_get(self):
        # checks the HTTP 200 status and amount of items=1 in queryset
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_post_get_anonymous(self):
        # checks the HTTP 200 status and amount of items=1 in queryset
        response = self.client_anonymous.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_post_like(self):
        request = self.client.put(
            '/post/{}/'.format(self.post.id), 
            data=self.payload_like, 
            follow = True
        )
        self.assertEqual(request.status_code, 200)
        post_like = PostLikes.objects.get(user=self.user, post=self.post)
        self.assertTrue(isinstance(post_like, PostLikes))

    def test_post_unlike(self):
        request = self.client.put(
            '/post/{}/'.format(self.post.id), 
            data=self.payload_unlike, 
            follow = True
        )
        self.assertEqual(request.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            PostLikes.objects.get(user=self.user, post=self.post)

    def test_post_unlike_after_liked(self):
        PostLikes.objects.create(**self.payload_post_like)
        request = self.client.put(
            '/post/{}/'.format(self.post.id), 
            data=self.payload_unlike, 
            follow = True
        )
        self.assertEqual(request.status_code, 200)
        with self.assertRaises(ObjectDoesNotExist):
            PostLikes.objects.get(user=self.user, post=self.post)


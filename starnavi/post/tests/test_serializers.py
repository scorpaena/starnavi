from django.test import TestCase
from post.serializers import PostSerializer, PostLikesSerializerByDate

class PostSerializerTestCase(TestCase):
    maxDiff = None
    
    def setUp(self):

        self.data = {
            'title': 'foo',
            'content': 'bar',
        }

        self.data_invalid = {
            'title': '',
            'content': '',
        }

        self.queryset = {
            "queryset": {
                "post": 2,
                "likes": 1
            }
        }

    def test_post_data(self):
        post = PostSerializer(data=self.data)
        self.assertTrue(post.is_valid())

    def test_post_data_invalid(self):
        post = PostSerializer(data=self.data_invalid)
        self.assertFalse(post.is_valid())

    def test_post_by_date(self):
        get_by_date = PostLikesSerializerByDate()
        self.assertEqual(
            get_by_date.get_queryset(queryset=self.queryset), self.queryset
        )
        

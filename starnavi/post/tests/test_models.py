from django.test import TestCase
from datetime import date
from user.models import User
from post.models import Post, PostLikes

today = date.today()

class PostModelTest(TestCase):
    maxDiff = None
    
    @classmethod
    def setUpTestData(cls):

        user = User.objects.create_user(
            email='foo@bar.com', 
            nickname = 'foo', 
            password='bar'
        )

        post = Post.objects.create(
            title='foo',
            content='bar',
            date_posted=today,
            author=user
        )

        post_like = PostLikes.objects.create(
            user=user,
            post=post,
            date_liked=today
        )

#======Post=========
    def test_post_title_label(self):
        post = Post.objects.get(id=1)
        title = post._meta.get_field('title').verbose_name
        self.assertEqual(title, 'title')

    def test_post_content_label(self):
        post = Post.objects.get(id=1)
        content = post._meta.get_field('content').verbose_name
        self.assertEqual(content, 'content')

    def test_post_dated_posted_label(self):
        post = Post.objects.get(id=1)
        date_posted = post._meta.get_field('date_posted').verbose_name
        self.assertEqual(date_posted, 'date posted')

    def test_post_author_label(self):
        post = Post.objects.get(id=1)
        author = post._meta.get_field('author').verbose_name
        self.assertEqual(author, 'author')

    def test_post_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_post_date_posted_auto_now_add(self):
        post = Post.objects.get(id=1)
        date_posted = post._meta.get_field('date_posted').auto_now_add
        self.assertEqual(date_posted, True)

    def test_post_object_name(self):
        post = Post.objects.get(id=1)
        title = post.title
        self.assertEqual(title, str(post))

#======PostLikes=========
    def test_post_like_post_label(self):
        post_like = PostLikes.objects.get(id=1)
        post = post_like._meta.get_field('post').verbose_name
        self.assertEqual(post, 'post')

    def test_post_like_user_label(self):
        post_like = PostLikes.objects.get(id=1)
        user = post_like._meta.get_field('user').verbose_name
        self.assertEqual(user, 'user')

    def test_post_like_dated_liked_label(self):
        post_like = PostLikes.objects.get(id=1)
        date_liked = post_like._meta.get_field('date_liked').verbose_name
        self.assertEqual(date_liked, 'date liked')

    def test_post_like_date_liked_auto_now(self):
        post_like = PostLikes.objects.get(id=1)
        date_liked = post_like._meta.get_field('date_liked').auto_now
        self.assertEqual(date_liked, True)

    def test_post_like_plural(self):
        verbose_name_plural = PostLikes._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'PostLikes')

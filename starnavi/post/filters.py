import django_filters as filters
from .models import Post

class PostListFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'id': ['exact',],
            'author__nickname': ['contains',],
            'title': ['contains',],
            'content': ['contains',],
            'date_posted': ['contains',],
        }

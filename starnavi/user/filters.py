import django_filters as filters
from .models import User

class UserListFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'id': ['exact',],
            'email': ['contains',],
            'nickname': ['contains',],
            'first_name': ['contains',],
            'last_name': ['contains',],
            'last_login': ['exact', 'year__gt'],
        }

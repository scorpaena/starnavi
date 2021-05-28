from rest_framework import serializers
from .models import Post, PostLikes


class PostSerializer(serializers.ModelSerializer):
    published_by = serializers.CharField(source='author', read_only=True)
    class Meta:
        model = Post
        exclude = ['author']


class PostDetailSerializer(serializers.ModelSerializer):
    VOTES = [
        ('like', 'like'),
        ('unlike', 'unlike')
    ]
    published_by = serializers.CharField(source='author', read_only=True)
    like_unlike = serializers.ChoiceField(choices=VOTES, write_only=True)
    class Meta:
        model = Post
        read_only_fields = ['title', 'content']
        exclude = ['author']


class PostLikesSerializer(serializers.ModelSerializer):
    liked_by = serializers.CharField(source='user', read_only=True)
    post = serializers.CharField(read_only=True)
    class Meta:
        model = PostLikes
        exclude = ['user']


class PostLikesSerializerByDate(serializers.Serializer):
    queryset = serializers.SerializerMethodField()

    def get_queryset(self, queryset):
        return queryset

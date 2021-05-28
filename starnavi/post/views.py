from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from .models import Post, PostLikes
from .filters import PostListFilter
from .serializers import (
    PostSerializer,
    PostLikesSerializer,
    PostDetailSerializer,
    PostLikesSerializerByDate
)


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]
    filterset_class = PostListFilter
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        obj = get_object_or_404(Post, pk=self.kwargs.get('post'))
        return obj

    def perform_update(self, serializer):
    # this function is to avoid multiple likes of a post by a single user
        like_unlike = serializer.validated_data.get('like_unlike')
        user = self.request.user
        post = self.get_object()
        if like_unlike == 'like':
            PostLikes.objects.get_or_create(user=user, post=post)[0]
        else:
            try:
                PostLikes.objects.get(user=user, post=post).delete()
            except ObjectDoesNotExist:
                pass
        return super().perform_update(serializer)


class PostLikesListView(generics.ListAPIView):
    queryset = PostLikes.objects.all().order_by('-date_liked')
    serializer_class = PostLikesSerializer


class PostLikesListViewByDate(generics.ListAPIView):
    serializer_class = PostLikesSerializerByDate

    def get_queryset(self):
        date_from = self.kwargs.get('from')
        date_to = self.kwargs.get('to')
        queryset = PostLikes.objects.values('post').filter(
            date_liked__gte = date_from, 
            date_liked__lte = date_to
        ).annotate(likes=Count('post')).order_by('-date_liked')
        return queryset

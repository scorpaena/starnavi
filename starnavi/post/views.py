from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from user.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.timezone import datetime
from django.contrib.sessions.models import Session
from .models import Post, PostLikes
# from .filters import PostFilter
from .serializers import (
    PostSerializer,
    PostLikesSerializer,
    PostDetailSerializer,
    PostLikesSerializerByDate
)


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date_posted')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    # filterset_class = PostFilter


class PostDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = PostDetailSerializer
    # filterset_class = PostFilter
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self):
        obj = get_object_or_404(Post, pk=self.kwargs.get('post'))
        return obj

    def perform_update(self, serializer):
    # this function is to avoid multiple likes of a post by a single user
        like_unlike = self.request.data.get('like_unlike')
        user = self.request.user
        post = self.get_object()
        if like_unlike == 'like':
            try:
                PostLikes.objects.get(user=user, post=post)
            except ObjectDoesNotExist:
                PostLikes.objects.create(user=user, post=post)
        else:
            try:
                PostLikes.objects.get(user=user, post=post)
            except ObjectDoesNotExist:
                pass
            else:
                PostLikes.objects.get(user=user, post=post).delete()
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
        ).annotate(likes=Count('post')).order_by('date_liked')
        return queryset

from django.contrib import admin
from .models import Post, PostLikes


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'content', 'date_posted')
    list_filter = ('author', 'title', 'content', 'date_posted')
    search_fields = ('author__nickname', 'title', 'content', 'date_posted')
    ordering = ('-date_posted',)


class PostLikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_liked')
    list_filter = ('user', 'post', 'date_liked')
    search_fields = ('user__nickname', 'post__title', 'date_liked')
    ordering = ('-date_liked',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostLikes, PostLikesAdmin)

from django.contrib import admin
from django.urls import path, include

# from .views import (Login, logout_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('user/', include('user.urls')),
    path('post/', include('post.urls')),
]

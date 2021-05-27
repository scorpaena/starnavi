from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserSignUpView, 
    LoginAndTokenObtain, 
    logout_view,
    UserLastLoginTimeView,
)

urlpatterns = [
    path('signup/', UserSignUpView.as_view()),
    path('login/', LoginAndTokenObtain.as_view()),
    path('logout/', logout_view),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('lastlogin/', UserLastLoginTimeView.as_view()),
]

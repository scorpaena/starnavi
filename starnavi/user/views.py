from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSignUpSerializer, UserLastLoginTimeSerializer
from .filters import UserListFilter
from .models import User


class UserSignUpView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer


class UserLastLoginTimeView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-last_login')
    serializer_class = UserLastLoginTimeSerializer
    filterset_class = UserListFilter
    permission_classes = [IsAdminUser,]


class LoginAndTokenObtain(TokenObtainPairView):
    '''TokenObtainPairView inherits from GenericAPIView and returns 
    "access" and "refresh" JSON web token pair. This class was customized
    to get the JSON web token pair right after user has been logged-in
    '''
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            response = {'error': 'email/password is wrong or user is disabled'}
            return Response(response, status=HTTP_403_FORBIDDEN)
        else:
            login(request, user)
            return super().post(request, *args, **kwargs)

def logout_view(request):
    logout(request)
    response = {'you are logged out'}
    return HttpResponse(response)

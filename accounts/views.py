from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from accounts.token_generator import generate_token
from rest_framework.views import APIView


@api_view(['GET'])
def profile(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return Response({'user': serialized_user})


class LoginView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    authentication_classes = []

    def post(self, request):
        User = get_user_model()
        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'email and password required')

        user = User.objects.filter(email=email).first()
        if (user is None):
            raise exceptions.AuthenticationFailed('user not found')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
        access_token = generate_token(user, day=0, min=30)
        refresh_token = generate_token(user, day=7, min=0)
        user = UserSerializer(user).data
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user
        }
        return response


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    http_method_names = 'post'
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        pass1 = request.data.get('password')
        pass2 = request.data.get('confirm_password')
        if email is None or username is None:
            raise exceptions.AuthenticationFailed('Email and Username is required')
        if pass1 is None or pass2 is None:
            raise exceptions.AuthenticationFailed('password is required')
        if pass1 != pass2:
            raise exceptions.AuthenticationFailed('Password and confirm password not matched!')
        User = get_user_model()
        user = User.objects.create_user(email=email, username=username, password=pass1)
        return Response("Registration successfully Done!!")

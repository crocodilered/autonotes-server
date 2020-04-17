from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import generics, views
from rest_framework.response import Response
from .serializers import UserCurrentSerializer, UserRegisterSerializer


User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    model = User
    serializer_class = UserRegisterSerializer


class UserCurrentView(generics.RetrieveAPIView):
    model = User
    serializer_class = UserCurrentSerializer

    def get_object(self):
        return self.request.user


class UserUpdatePasswordView(views.APIView):
    model = User

    def post(self, request, *args, **kwargs):
        user = self.request.user
        password0 = request.data.get('current_password')
        password1 = request.data.get('new_password1')
        password2 = request.data.get('new_password2')

        if not(password0 and password1 and password1 == password2):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password0):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user.set_password(password1)
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

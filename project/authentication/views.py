from functools import partial
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User, Group
from .serializers import RegisterSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import ExtendedUserModel
from django.shortcuts import get_object_or_404
import string
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ForgetPassword(APIView):

    def patch(self,request):
        print(request.data)
        username = request.data["username"]
        user = User.objects.get(username = username)
        user.set_password(request.data["password"])
        user.save()

        return Response("Success")
        

class GetToken(APIView):

    permission_classes = [ IsAuthenticated ]

    def get(self,request):
        user = User.objects.get(username = request.user)
        userserializer = UserSerializer(user)
        group = Group.objects.filter(user = request.user)

        user_res = userserializer.data
        user_res["user_type"] = group[0].name
        return Response(user_res)

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


    def post( self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.__dict__["_kwargs"]["data"]["username"]
        try :
            extended_user = ExtendedUserModel.objects.get(user__username = username)
            user = User.objects.get(username = extended_user.user)
            user_response = {
                "username" : extended_user.user.username,
                "email" : extended_user.user.email,
                "user_type" : extended_user.user_type
            }
            response = {
                "user" : user_response,
                "token" : serializer.__dict__['_validated_data']
            }
            password = id_generator(100)
            user.set_password(password)
            user.save()
            return Response(response)
        except :
            return Response("No user found", status=status.HTTP_404_NOT_FOUND)



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # simply delete the token to force a login
        refresh_token = RefreshToken.objects.all()
        return Response(status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = ExtendedUserModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



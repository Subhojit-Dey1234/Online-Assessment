from .serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User, Group
from .serializers import RegisterSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.shortcuts import get_object_or_404



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

        user = User.objects.filter(username = username)
        group = Group.objects.filter(user__username = username)
        user_response = {
            "username" : user[0].username,
            "email" : user[0].email,
            "user_type" : group[0].name,
        }
        
        response = {
            "user" : user_response,
            "token" : serializer.__dict__['_validated_data']
        }
        return Response(response)



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # simply delete the token to force a login
        refresh_token = RefreshToken.objects.all()
        return Response(status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
from .serializers import MyTokenObtainPairSerializer, UserSerializer, LogoutSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User, Group
from .serializers import RegisterSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import ExtendedUserModel
from rest_framework import status

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
        print(request.data)
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.__dict__["_kwargs"]["data"]["username"]
        try :
            extended_user = ExtendedUserModel.objects.get(user__username = username)
            user = User.objects.get(username = extended_user.user)
            print(extended_user.profile)
            user_response = {
                "username" : extended_user.user.username,
                "email" : extended_user.user.email,
                "user_type" : extended_user.user_type,
                "mobile_number" : extended_user.mobile_number,
                "telephone_number" : extended_user.telephone_number,
                "city_name" : extended_user.city_name,
                "street_name" : extended_user.street_name,
                "state_name" : extended_user.state_name,
                "country" : extended_user.country,
                "zip_code" : extended_user.zip_code,
                "profile" : '/media/' + str(extended_user.profile),
                "first_name" : extended_user.user.first_name,
                "last_name" : extended_user.user.last_name
            }
            response = {
                "user" : user_response,
                "token" : serializer.__dict__['_validated_data']
            }
            user.save()
            return Response(response)
        except :
            return Response("No user found", status=status.HTTP_404_NOT_FOUND)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

class RegisterView(APIView):
    queryset = ExtendedUserModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self,request):
        register_ser = self.serializer_class(data = request.data)
        if(register_ser.is_valid()):
            register_ser.save()
            return Response(register_ser.data,status= status.HTTP_201_CREATED)
        return Response(register_ser.errors,status= status.HTTP_500_INTERNAL_SERVER_ERROR)



class EditProfile(APIView):
    queryset = ExtendedUserModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterSerializer

    def patch(self,request):
        # try:
        validated_data = request.data
        # username = ExtendedUserModel.objects.get(user__username = request.data["username"])
        user = User.objects.get(username = validated_data["username"])
        user.first_name = validated_data["first_name"] if "first_name" in validated_data else user.first_name
        user.last_name = validated_data["last_name"] if "last_name" in validated_data else user.last_name
        user.save()


        extended_user = ExtendedUserModel.objects.get(user = user)
        extended_user.city_name = validated_data["city_name"] if "city_name" in validated_data else extended_user.city_name
        extended_user.street_name = validated_data["street_name"] if "street_name" in validated_data else extended_user.street_name
        extended_user.state_name = validated_data["state_name"] if "state_name" in validated_data else extended_user.state_name
        extended_user.country = validated_data["country"] if "country" in validated_data else extended_user.country
        extended_user.zip_code = validated_data["zip_code"] if "zip_code" in validated_data else extended_user.zip_code
        extended_user.mobile_number = validated_data["mobile_number"] if "mobile_number" in validated_data else extended_user.mobile_number
        extended_user.telephone_number = validated_data["telephone_number"] if "telephone_number" in validated_data else extended_user.telephone_number
        extended_user.father_name = validated_data["father_name"] if "father_name" in validated_data else extended_user.father_name
        extended_user.aadhar_number = validated_data["aadhar_number"] if "aadhar_number" in validated_data else extended_user.aadhar_number
        extended_user.profile = validated_data["profile"] if "profile" in validated_data else extended_user.profile
        extended_user.save()

        serializer = RegisterSerializer(extended_user)
        return Response(serializer.data)



from matplotlib.style import use
from numpy import source
from requests import request
from assessment.models import Student, Teacher
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password
from .models import ExtendedUserModel
from rest_framework_simplejwt.tokens import RefreshToken
import string
import random


def id_generator(
    size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
):
    return "".join(random.choice(chars) for _ in range(size))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        source="user.email",
    )
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    city = serializers.CharField(required = False)
    state = serializers.CharField(required = False)
    discipline = serializers.CharField(required = False)
    programme = serializers.CharField(required = False)

    class Meta:
        model = ExtendedUserModel
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "city",
            "state",
            "discipline",
            "programme"
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["user"]["username"],
            email=validated_data["user"]["email"],
            first_name=validated_data["user"]["first_name"],
            last_name=validated_data["user"]["last_name"],
        )

        extended_user = ExtendedUserModel.objects.create(
            user=user,
            phone_number=validated_data["phone_number"],
            user_type=validated_data["user_type"],
        )

        user.set_password(id_generator(100))

        user_type = validated_data["user_type"]
        dis_f = validated_data["discipline"] if  "discipline" in validated_data else ""
        prog_f = validated_data["programme"] if  "programme" in validated_data else ""
        st_f = validated_data["state"] if "state" in validated_data else ""
        if user_type == "student":
            st = Student.objects.create(
                user=user, city=validated_data["city"], state = st_f,
                discipline = dis_f,
                programme = prog_f
            )
            st.save()
        elif user_type == "teacher":
            tch = Teacher.objects.create(
                user=user, city = validated_data["city"], state=st_f
            )
            tch.save()

        user.save()
        extended_user.save()
        return extended_user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        RefreshToken(self.token).blacklist()

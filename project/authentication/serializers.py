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
from rest_framework import status
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
    state_name = serializers.CharField(required = False)
    mobile_number = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=ExtendedUserModel.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = ExtendedUserModel
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "city_name",
            "street_name",
            "state_name",
            "country",
            "zip_code",
            "mobile_number",
            "telephone_number",
            "father_name",
            "aadhar_number",
            "profile",
            "password",
            "password2"
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["user"]["username"],
            email=validated_data["user"]["email"],
            first_name=validated_data["user"]["first_name"],
            last_name=validated_data["user"]["last_name"],
        )

        user.set_password(validated_data['password'])
        extended_user = ExtendedUserModel.objects.create(
            user=user,
            mobile_number=validated_data["mobile_number"],
            telephone_number=validated_data["telephone_number"],
            father_name=validated_data["father_name"],
            user_type=validated_data["user_type"],
            street_name=validated_data["street_name"],
            city_name=validated_data["city_name"],
            state_name=validated_data["state_name"],
            aadhar_number = validated_data["aadhar_number"],
            country=validated_data["country"],
            zip_code=validated_data["zip_code"]
        )

        user_type = validated_data["user_type"]

        
        if user_type == "student":
            st = Student.objects.create(
                user=user
            )
            st.save()
        elif user_type == "teacher":
            tch = Teacher.objects.create(
                user=user
            )
            tch.save()

        user.save()
        extended_user.save()
        return extended_user

    def update(self, instance, validated_data):
        print(validated_data)
        user = User.objects.get(username = validated_data["user"]["username"])
        user.first_name = validated_data["user"]["first_name"] if validated_data["user"]["first_name"] else user.first_name
        user.last_name = validated_data["user"]["last_name"] if validated_data["user"]["last_name"] else user.last_name
        user.save()

        extended_user = ExtendedUserModel.objects.get(user = user)
        extended_user.city_name = validated_data["city_name"] if validated_data["city_name"] else extended_user.city_name
        extended_user.street_name = validated_data["street_name"] if validated_data["street_name"] else extended_user.street_name
        extended_user.state_name = validated_data["state_name"] if validated_data["state_name"] else extended_user.state_name
        extended_user.country = validated_data["country"] if validated_data["country"] else extended_user.country
        extended_user.zip_code = validated_data["zip_code"] if validated_data["zip_code"] else extended_user.zip_code
        extended_user.mobile_number = validated_data["mobile_number"] if validated_data["mobile_number"] else extended_user.mobile_number
        extended_user.telephone_number = validated_data["telephone_number"] if validated_data["telephone_number"] else extended_user.telephone_number
        extended_user.father_name = validated_data["father_name"] if validated_data["father_name"] else extended_user.father_name
        extended_user.aadhar_number = validated_data["aadhar_number"] if validated_data["aadhar_number"] else extended_user.aadhar_number
        extended_user.profile = validated_data["profile"]

        extended_user.save()

        return extended_user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        RefreshToken(self.token).blacklist()

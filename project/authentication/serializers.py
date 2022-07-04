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



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username","email")

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username','password', 'password2', 'email', 'first_name', 'last_name','groups')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')

        
        user = User.objects.create(
            username = validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.groups.add(groups_data[0])
        user.set_password(validated_data['password'])
        

        if( groups_data[0].name == "Students"):
            student = Student.objects.create( user = user )
            student.save()

        elif ( groups_data[0].name == "Teacher"):
            teacher = Teacher.objects.create( user = user )
            teacher.save()

        user.save()
        return user
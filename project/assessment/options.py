from functools import partial
from rest_framework.response import Response
from .serializers import OptionSerializer, QuestionSerializer, TestSerializer
from .models import Attempts, Option, Question, Student, Submission, Test
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class Option_View(APIView):

    def get(self,request,pk):
        option = Option.objects.get(pk = pk)
        optionserializer = QuestionSerializer(option)

        return Response(optionserializer.data,status=status.HTTP_200_OK)


    def delete(self,request,pk):
        option = Option.objects.get(pk = pk)
        option.delete()
        return Response("Success",status=status.HTTP_200_OK)


    def patch(self,request,pk):
        option = Option.objects.get(pk = pk)
        optionserializer = OptionSerializer(option, data=request.data, partial = True)
        if(optionserializer.is_valid()):
            optionserializer.save()
            return Response(optionserializer.data , status= status.HTTP_200_OK)
        return Response(optionserializer.errors , status= status.HTTP_400_BAD_REQUEST)
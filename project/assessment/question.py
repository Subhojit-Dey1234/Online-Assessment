from rest_framework.response import Response
from .serializers import QuestionSerializer, TestSerializer
from .models import Attempts, Option, Question, Student, Submission, Test
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class Question_View(APIView):

    def get(self,request,pk):
        question = Question.objects.get(pk = pk)
        questionserializer = QuestionSerializer(question)

        return Response(questionserializer.data,status=status.HTTP_200_OK)

    def delete(self,request,pk):
        question = Question.objects.get(pk = pk)
        question.delete()
        return Response("Success",status=status.HTTP_200_OK)


    def patch(self,request,pk):
        question = Question.objects.get(pk = pk)
        questionserializer = QuestionSerializer(question, data=request.data, partial = True)
        if(questionserializer.is_valid()):
            questionserializer.save()
            return Response(questionserializer.data , status= status.HTTP_200_OK)
        return Response(questionserializer.errors , status= status.HTTP_400_BAD_REQUEST)



class Question_View_Post(APIView):

    def post(self,request):
        data = request.data
        question = Question.objects.create()
        question.test = Test.objects.get(pk = data["test"])
        question.name = data["name"]
        question.positive_marks = data["positive_marks"]
        question.negative_marks = data["negative_marks"]
        options = data["options"]

        for option in options:
            question.options.add(Option.objects.get(pk = option))

        question.save()

        return Response("Success",status=status.HTTP_200_OK)

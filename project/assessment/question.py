from rest_framework.response import Response

from authentication.models import ExtendedUserModel
from .serializers import QuestionSerializer, TestSerializer
from .models import Attempts, Option, Question, Student, Submission, Test
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group


class Question_View(APIView):

    def get(self,request,pk):
        try :
            question = Question.objects.get(pk = pk)
            questionserializer = QuestionSerializer(question)

            return Response(questionserializer.data,status=status.HTTP_200_OK)
        except :
            return Response("Not Found", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,pk):
        question = Question.objects.get(pk = pk)
        question.delete()
        return Response("Success",status=status.HTTP_200_OK)


    def patch(self,request,pk):
        options = request.data["options"]
        question = Question.objects.get(pk = pk)
        question.options.set([])
        for op in options:
            try :
                op_obj = Option.objects.get(pk = op)
                question.options.add(op_obj)
            except :
                return Response("Options Not found", status=status.HTTP_404_NOT_FOUND)
        del request.data["options"]
        questionserializer = QuestionSerializer(question, data= request.data, partial = True)
        if(questionserializer.is_valid()):
            questionserializer.save()
            return Response(questionserializer.data , status= status.HTTP_200_OK)
        return Response(questionserializer.errors , status= status.HTTP_400_BAD_REQUEST)



class Question_View_Post(APIView):

    def post(self,request):
        for key in request.data:
            if( key != 'exam_end_time' and key != 'exam_start_time' and request.data[key] == None ):
                return Response("Empty Field is not allowed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user = ExtendedUserModel.objects.get(user = request.user)
        if(user.user_type == "student"):
            return Response("You are not allowed....",status.HTTP_400_BAD_REQUEST)
        data = request.data
        question = Question.objects.create()
        test = Test.objects.get(unique_id = data["test"])
        question.test = test
        question.name = data["name"]
        question.positive_marks = data["positive_marks"]
        question.negative_marks = data["negative_marks"]
        options = data["options"]
        question.is_range_present = data["is_range_present"]

        if(question.is_range_present) :
            question.lowest_mark = data["lowest_mark"]
            question.highest_mark = data["highest_mark"]

        for option in options:
            op = Option.objects.create(
                question = question,
                name = option["name"],
                is_correct = option["is_correct"]
            )
            op.save()
            question.options.add(op)
        question.save()
        test.questions.add(question)
        question_serializer = QuestionSerializer(question)

        return Response(question_serializer.data,status=status.HTTP_200_OK)

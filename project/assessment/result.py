from rest_framework.response import Response
from sympy import false
from .serializers import AttemptSerializer, QuestionSerializer, TestSerializer
from .models import Attempts, Option, Question, Student, Submission, Test
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attempts
        fields = "__all__"


# For Student
class Result(APIView):

    permission_classes = [ IsAuthenticated ]

    def get(self,request,pk):
        test = Test.objects.get(unique_id = pk)
        if not test.show_result:
            return Response("Result is not available currenlty",status=status.HTTP_404_NOT_FOUND)
        attempts = Attempts.objects.filter(test__unique_id = pk, student__user = request.user)
        attempt_ser = ResultSerializer(attempts,many = True)
        return Response(attempt_ser.data, status=status.HTTP_200_OK)


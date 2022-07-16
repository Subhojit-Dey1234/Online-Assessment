from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TestSerializer
from .models import Attempts, Option, Question, Student, Submission, Test
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Overall

class Student_Ranking(APIView):

    def get(self,request,pk):
        test  = Test.objects.get(unique_id = pk)
        test_serialiser = TestSerializer(test)
        return Response(test_serialiser.data["submission"])
from django.http import Http404
# Create your views here.
from .serializers import (
    SubmissionSerializer,
    AttemptSerializer,
    TestSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Attempts, Option, Question, Student, Submission, Test
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class Test_View_Details(APIView):

    permission_classes = [ IsAuthenticated ]


    def get_object(self,pk):
        test = Test.objects.filter(unique_id = pk)
        test_serializer = TestSerializer(test)
        return Response(test_serializer.data, status=status.HTTP_202_ACCEPTED)

    def get(self, request, *args, **kwargs):
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

    def post(self, request):
        if(request.user.groups.all()[0].name == "Students"):
            return Response("You are not allowed", status=status.HTTP_401_UNAUTHORIZED)
        try:
            data = JSONParser().parse(request)
            name = data["name"]
            isFixed = data["isFixed"]
            exam_start_time = data["exam_start_time"]
            exam_end_time = data["exam_end_time"]
            test = Test.objects.create(
                name=name,
                isFixed=isFixed,
                exam_start_time=exam_start_time,
                exam_end_time=exam_end_time,
            )
            test.save()
            questions = data["questions"]
            for question in questions:
                question_data = Question.objects.create(name=question["name"])
                options = question["options"]
                for op in options:
                    option_data = Option.objects.create(
                        name=op["name"], is_correct=op["is_correct"]
                    )
                    question_data.options.add(option_data)
                    option_data.question = question_data
                    option_data.save()

                question_data.test = test
                question_data.save()
                test.questions.add(question_data)
            test_serializer = TestSerializer(test)
            return Response(test_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class Test_View_Detail_Single(APIView):
    

    permission_classes = [ IsAuthenticated ]

    def get_object(self,pk):
        test = Test.objects.filter(unique_id = pk)
        if test :
            return test
        raise Http404

    def get(self,request,pk):
        test = self.get_object(pk)
        test_serializer = TestSerializer(test,many = True)
        return Response(test_serializer.data, status=status.HTTP_200_OK)

    def delete(self,pk):
        test = self.get_object(pk)
        test.delete()
        return Response("Deleted Successfully", status=status.HTTP_200_OK)

class Submission_View_All(APIView):

    permission_classes = [ IsAuthenticated ]

    def get(self,request):
        submissions = Submission.objects.all()
        return Response(SubmissionSerializer(submissions,many=True).data,status=status.HTTP_200_OK)


class Submission_View(APIView):

    permission_classes = [ IsAuthenticated ]

    def get_object(self,pk):
        test = Test.objects.filter(unique_id = pk)
        if test :
            return test
        raise Http404

    def get(self,request,pk = None):
        submissions = Submission.objects.get(pk = pk)
        serializer = SubmissionSerializer(submissions)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,pk):
        if(request.user.groups.all()[0].name == "Students"):
            return Response("You are not allowed", status=status.HTTP_401_UNAUTHORIZED)
        submissions = request.data["submissions"]
        test = self.get_object(pk)
        attempt = Attempts.objects.create(
            name = request.data["name"]
        )
        attempt.test = test[0]
        marks_obtained = 0
        for submission in submissions:
            question = Question.objects.get(pk = submission["question"])
            submsm = Submission.objects.create()
            submsm.question = question
            for answer in submission["answer_submitted"]:
                submitted_option = Option.objects.get(pk = answer)
                submsm.answer_submitted.add(submitted_option)
                if submitted_option.is_correct:
                    marks_obtained += question.positive_marks
                else:
                    marks_obtained -= question.negative_marks
            submsm.save()
            attempt.submission.add(submsm)
            attempt.marks_obtained = marks_obtained
        attempt.save()
        serailizer = AttemptSerializer(attempt)
        return Response(serailizer.data)


class Attempts_View(APIView):

    permission_classes = [ IsAuthenticated ]

    def get(self,request,pk = None):
        
        attempt = Attempts.objects.get(pk = pk)
        serializer = AttemptSerializer(attempt)
        return Response(serializer.data,status=status.HTTP_200_OK)
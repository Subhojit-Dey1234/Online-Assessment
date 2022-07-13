from django.http import Http404
# Create your views here.
from .serializers import (
    SubmissionSerializer,
    AttemptSerializer,
    TestSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Attempts, Option, Question, Student, Submission, Teacher, Test
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from authentication.models import ExtendedUserModel


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
        user = ExtendedUserModel.objects.get(user = request.user)
        if(user.user_type == "student"):
            return Response("You are not allowed", status=status.HTTP_401_UNAUTHORIZED)
        try:
            teacher = Teacher.objects.filter(user = request.user)
            data = JSONParser().parse(request)
            students = data["students"]                
            name = data["name"]
            isFixed = data["isFixed"]
            exam_start_time = data["exam_start_time"]
            exam_end_time = data["exam_end_time"]
            test = Test.objects.create(
                teacher = teacher[0],
                name=name,
                isFixed=isFixed,
                exam_start_time=exam_start_time,
                exam_end_time=exam_end_time,
            )

            if( len(students) == 0 ):
                for s in Student.objects.all():
                    test.student.add(s)
                    s.alloted_test.add(test)

            else:
                for s in students:
                    s_email = Student.objects.filter(user__email = s)
                    print(s_email)
                    if s_email:
                        test.student.add(s_email[0])
                        s_email[0].alloted_test.add(test)
            test.save()
            questions = data["questions"]
            for q in questions:
                question_data = Question.objects.get(pk = q)
                # print(question_data[0])
                test.questions.add(question_data)
                question_data.test = test
                question_data.save()
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
        test = Test.objects.filter(unique_id = pk)
        if test:
            test_serializer = TestSerializer(test[0])
            return Response(test_serializer.data, status=status.HTTP_200_OK)
        return Response("Not found", status=status.HTTP_404_NOT_FOUND)

    def patch(self,request,pk):
        ques = request.data["questions"]
        test = Test.objects.get(unique_id = pk)
        test.questions.set([])
        for q in ques:
            qs = Question.objects.get(pk = q)
            test.questions.add(qs)
        del request.data["questions"]
        test_serializer = TestSerializer(test, data = request.data, partial = True)
        if(test_serializer.is_valid()):
            test_serializer.save()
            return Response(test_serializer.data,status= status.HTTP_200_OK)
        return Response(test_serializer.errors,status=status.HTTP_404_NOT_FOUND)

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
        submissions = Attempts.objects.get(pk = pk)
        serializer = AttemptSerializer(submissions)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,pk):
        student = Student.objects.get(user = request.user)
        test = self.get_object(pk)[0]
        if test in student.attempted_test.all():
            return Response("You have already attempted", status=status.HTTP_404_NOT_FOUND)
        student.attempted_test.add(test)
        submissions = request.data["submissions"]
        test = self.get_object(pk)
        attempt = Attempts.objects.create(
            name = request.data["name"]
        )
        attempt.test = test[0]
        test[0].submission.add(attempt)

        attempt.student = student
        marks_obtained = 0
        for submission in submissions:
            question = Question.objects.get(pk = submission["question"])
            # Creating Submission Object for submitting Question
            submsm = Submission.objects.create()
            submsm.question = question
            is_question_correct = True
            for answer in submission["answer_submitted"]:
                submitted_option = Option.objects.get(pk = answer)
                is_question_correct = is_question_correct and submitted_option.is_correct
                submsm.answer_submitted.add(submitted_option)

            if is_question_correct:
                attempt.marks_obtained += question.positive_marks
            else:
                attempt.marks_obtained -= question.negative_marks
            
            submsm.save()
            attempt.submission.add(submsm)
        attempt.save()
        serailizer = AttemptSerializer(attempt)
        return Response(serailizer.data, status=status.HTTP_201_CREATED)


class Attempts_View(APIView):

    permission_classes = [ IsAuthenticated ]

    def get(self,request,pk = None):
        
        attempt = Attempts.objects.get(pk = pk)
        serializer = AttemptSerializer(attempt)
        return Response(serializer.data,status=status.HTTP_200_OK)



class CheckSubmission(APIView):

    def get(self,request,pk):
        student = Student.objects.get(user = request.user)
        test = Test.objects.get(unique_id = pk)
        print(test)
        if test in student.attempted_test.all():
            return Response("You have already submitted",status=status.HTTP_200_OK)
        if test in student.alloted_test.all():
            return Response("Can attempt",status=status.HTTP_200_OK)
        return Response("Not Allowed",status=status.HTTP_405_METHOD_NOT_ALLOWED)
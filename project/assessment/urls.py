from django.contrib import admin
from django.urls import path,include, re_path

from .result import Result

from .options import Option_View, Option_Post

from .question import Question_View,Question_View_Post

from .ranking import Student_Ranking
from .views import Submission_View, Submission_View_Student_View, Test_Student, Test_View_Detail_Single, Test_View_Details,CheckSubmission,Submission_View_Student
from .test_upload import Test_Upload
urlpatterns = [
    path('tests_students/',Test_Student.as_view()),
    path('tests/<pk>/',Test_View_Detail_Single.as_view()),
    path('tests/',Test_View_Details.as_view()),
    path('test-upload/', Test_Upload.as_view()),
    path('questions/',Question_View_Post.as_view()),
    path('questions/<pk>/',Question_View.as_view()),
    path('options/',Option_Post.as_view()),
    path('options/<pk>/',Option_View.as_view()),
    path('submission/<test>/',Submission_View_Student.as_view()),
    path('submission/<test>/<pk>/',Submission_View_Student_View.as_view()),
    path('attempts/<pk>/',Submission_View.as_view()),
    path('ranking/<pk>/',Student_Ranking.as_view()),
    path('check_attempts/<pk>/',CheckSubmission.as_view()),
    path('result/<pk>/',Result.as_view()),
    
]
from django.contrib import admin
from django.urls import path,include, re_path
from .views import Submission_View, Test_View_Detail_Single, Test_View_Details

urlpatterns = [
    path('tests/<pk>/',Test_View_Detail_Single.as_view()),
    path('tests/',Test_View_Details.as_view()),
    path('submission/',Test_View_Details.as_view()),
    path('submission/<pk>/',Submission_View.as_view()),
    path('attempts/<pk>/',Submission_View.as_view())
]
from django.contrib import admin

from .models import Student, Teacher, Test, Question, Submission, Option, Attempts

# Register your models here.
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(Test)
admin.site.register(Option)
admin.site.register(Attempts)
admin.site.register(Teacher)
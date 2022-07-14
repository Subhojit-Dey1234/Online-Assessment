from ast import Try
from django.db import models
import uuid
from django.contrib.auth.models import User


class Teacher(models.Model):
    user = models.ForeignKey(User, blank= True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
    

class Test(models.Model):
    teacher = models.ForeignKey(Teacher,null=True,blank=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=300)
    unique_id = models.UUIDField(default=uuid.uuid4,max_length=5,editable = False)
    isFixed = models.BooleanField(default=False)
    exam_start_time = models.DateTimeField(null=True, blank=True)
    exam_end_time = models.DateTimeField(null=True, blank=True)
    student = models.ManyToManyField("Student",related_name="student_field")
    questions = models.ManyToManyField("Question", related_name="question")
    submission = models.ManyToManyField("Attempts", related_name="submission_field",blank=True)
    show_result = models.BooleanField(default=True)
    marks_obtained = models.IntegerField(default=0)
    instructions = models.CharField(max_length=1000, blank=True, null=True)

    # def __str__(self):
    #     return self.name


class Question(models.Model):
    test = models.ForeignKey(Test,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    options = models.ManyToManyField("Option",related_name="option",blank=True)
    positive_marks = models.IntegerField(default=0)
    negative_marks = models.IntegerField(default=0)
    is_range_present = models.BooleanField(default=False)
    lowest_mark = models.FloatField(default=0,blank=True)
    highest_mark = models.FloatField(default=0,blank=True)

    def __str__(self) -> str:
        return str(self.id)

class Option(models.Model):
    question = models.ForeignKey(Question,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.id)


class Attempts(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True,null=True,related_name="submission_test")
    name = models.CharField(max_length=300)
    student = models.ForeignKey("Student",on_delete=models.CASCADE,blank=True,null=True,related_name="student_submitted")
    submission =  models.ManyToManyField("Submission", related_name="submission_attempts_field")
    marks_obtained = models.IntegerField(default=0)

    # def __str__(self) -> str:
    #     return self.name

    

class Submission(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True,null=True,related_name="test")
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,blank=True,null=True,related_name="question_foreign_key")
    answer_submitted = models.ManyToManyField(Option, blank=True)
    subjective_answer = models.CharField(max_length=3000,blank=True,null=True)
    type = models.CharField(max_length=100,default="Fill in Blanks")
    is_correct = models.BooleanField(default=False)
    is_attempted = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)




class Student(models.Model):
    user = models.ForeignKey(User, blank= True, null=True, on_delete=models.CASCADE)
    attempted_test  = models.ManyToManyField(Test,related_name="test_field",blank=True)
    alloted_test  = models.ManyToManyField(Test,related_name="alloted_test",blank=True)
    

    def __str__(self):
        return self.user.username

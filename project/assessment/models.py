from ast import Try
from django.db import models
import uuid


class Test(models.Model):
    name = models.CharField(max_length=300)
    unique_id = models.UUIDField(default=uuid.uuid4,max_length=5,editable = False)
    isFixed = models.BooleanField(default=False)
    exam_start_time = models.DateField(null=True, blank=True)
    exam_end_time = models.DateField(null=True, blank=True)
    student = models.ManyToManyField("Student",related_name="student_field")
    questions = models.ManyToManyField("Question", related_name="question")
    submission = models.ManyToManyField("Submission", related_name="submission_field",blank=True)
    show_result = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    options = models.ManyToManyField("Option",related_name="option")
    positive_marks = models.IntegerField(default=0)
    negative_marks = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.id)

class Option(models.Model):
    question = models.ForeignKey(Question,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.id)


class Attempts(models.Model):
    name = models.CharField(max_length=300)
    student = models.ForeignKey("Student",on_delete=models.CASCADE,blank=True,null=True,related_name="student_submitted")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True,null=True,related_name="submission_test")
    submission =  models.ManyToManyField("Submission", related_name="submission_attempts_field")
    marks_obtained = models.IntegerField(default=0)

    # def __str__(self) -> str:
    #     return self.name

    

class Submission(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,blank=True,null=True,related_name="question_foreign_key")
    answer_submitted = models.ManyToManyField(Option, blank=True)
    subjective_answer = models.CharField(max_length=3000,blank=True,null=True)



class Student(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    test  = models.ManyToManyField(Test,related_name="test_field",blank=True)

    def __str__(self):
        return self.name

from cgi import test
from rest_framework import serializers
from .models import Attempts, Option, Question, Submission, Test, Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data)
        return Option.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        return question

    
class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    student = StudentSerializer(many=True)
    class Meta:
        model = Test
        fields = "__all__"
        



class SubmissionSerializer(serializers.ModelSerializer):
    answer_submitted = OptionSerializer(many=True)
    class Meta:
        model = Submission
        fields = "__all__"


class AttemptSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many = True)
    # question = QuestionSerializer()
    class Meta:
        model = Attempts
        fields = "__all__"
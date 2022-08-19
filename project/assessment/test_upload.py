import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from rest_framework import status

from .serializers import TestSerializer
from.models import Option, Question, Test

class Test_Upload(APIView):

    def split_string(self,s):
        return " ".join(str(s).split())


    def get_object(self,pk):
        print("sdfsd")
        test = Test.objects.filter(unique_id = pk)
        print(test)
        if test.first():
            return test
        print("Not found")
        raise Http404

    def post(self,request):
        unique_id = request.data["unique_id"]
        print(unique_id)
        test = None
        try:
            print("alkkasn")
            xls = pd.read_excel(request.data['file'],sheet_name = "MCQ",index_col=None, header=None)
            xls = xls.values.tolist()
            time_alloted = self.split_string(xls[13][1])
            total_marks = self.split_string(xls[13][3])

            time_alloted_n = ""
            for s in time_alloted:
                if(s.isdigit()):
                    time_alloted_n += s

            
            total_marks_n = ""
            for s in total_marks:
                if(s.isdigit()):
                    total_marks_n += s
            
            instructions_col = xls[15:]
            st = 15
            instructions = ""

            for inst in instructions_col:
                l = len(set(inst))
                st += 1
                if(l == 1):
                    break
                if(type(inst[1]) == str):
                    instructions += self.split_string(inst[1])
                    instructions += "\n"

            questions_detail = xls[st+2:30]
            print("alkkasn")
            if(len(time_alloted_n) == 0 or len(total_marks_n) == 0):
                return Response("Test Data is missiing")

            print("alkkasn")
            test = self.get_object(unique_id)[0]
            print(test)
            test.instructions = instructions
            test.time_alloted = int(time_alloted_n)
            test.total_marks = int(total_marks_n)

            print("TOtl")

            for questions in questions_detail:
                question_name = questions[2]
                question_model = Question.objects.create(
                    name = question_name,
                    test = test
                )
                test.questions.add(question_model)
                options = []
                for op in questions[3:7]:
                    if(type(op) != str):
                        break
                    options += [op]

                    op_m = Option.objects.create(
                        name = op,
                        question = question_model
                    )
                    question_model.options.add(op_m)

            print("TOtl")
            print(test)
            test_s = TestSerializer(test)
            return Response(test_s.data,status=status.HTTP_201_CREATED)
        except :
            if(test):
                test.delete()
            return Response("There is an error!",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
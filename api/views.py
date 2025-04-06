from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import QuestionSerializer
from tests.models import Question, TestResult

class GetTestQuestions(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        question_set = Question.objects.order_by("?")[:3]
        serializer = QuestionSerializer(question_set, many=True)
        return Response(serializer.data)

class SaveTestResults(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        mode = request.query_params.get('mode')
        result = request.data
        profile = request.user.profile
        test_length = len(result)
        correct_answer_count = 0
        for item in result:
            if item["answer"] in item["correct_answer"]:
                correct_answer_count += 1
        TestResult.objects.create(
            owner=profile,
            test_category = mode,
            score = round((correct_answer_count / test_length) * 100,0)
        )
        return Response(status=status.HTTP_200_OK)

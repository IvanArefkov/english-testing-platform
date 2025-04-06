from django.urls import path
from . import views


urlpatterns = [
    path('get_test_questions/', views.GetTestQuestions.as_view(), name="get_test_questions"),
    path('save_test_results/', views.SaveTestResults.as_view(), name="save_test_results"),
]
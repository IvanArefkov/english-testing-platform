from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.homePage,name="home"),
    path('uploadTests/',views.uploadTests,name="uploadTests"),
    path('test_welcome/',views.test_welcome,name="test_welcome"),
    path('test_page/<str:mode>',views.test_page,name="test_page"),
    path('get_test_questions/',views.get_test_questions,name="get_test_questions"),
]
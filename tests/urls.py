from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.homePage,name="home"),
    path('uploadTests/',views.uploadTests,name="uploadTests"),
    path('test_welcome/',views.test_welcome,name="test_welcome"),
    path('test_page/',views.test_page,name="test_page"),
]
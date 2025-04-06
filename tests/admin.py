from django.contrib import admin
from .models import Question, TestResult

# Register your models here.
admin.site.register(Question)
admin.site.register(TestResult)
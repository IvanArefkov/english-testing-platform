import time

from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from .forms import QuestionUploadForm
from .utils import *
import json


# Create your views here.

@login_required(login_url='login')
def homePage(request):
    context = {

    }
    return render(request, 'tests/home.html', context)
@login_required(login_url='login')
def uploadTests(request):
    form = QuestionUploadForm()
    context = {'form': form}
    if request.method == 'POST':
        form = QuestionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            questions_file = request.FILES['upload_file']
            validate_upload_questions(request, questions_file)
    return render(request,'tests/upload_questions.html',context)
@login_required(login_url='login')
def test_welcome(request):
    mode = request.GET.get('mode')
    context = {
        'mode': mode,
    }
    return render(request,'tests/test_welcome.html',context)
@login_required(login_url='login')
def test_page(request,mode):
    user = request.user.profile
    question_set = get_questions(request,mode)
    context = {
        'mode': mode,
        'question_set': question_set,
    }
    return render(request,'tests/test_page.html',context)

def get_test_questions(request):
    question_set = Question.objects.order_by("?")[:3]
    json_data = json.loads(serialize("json", question_set))
    return JsonResponse(json_data, safe=False)
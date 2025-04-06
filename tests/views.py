from django.shortcuts import render
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
def test_page(request):
    mode = request.GET.get('mode')
    user = request.user.profile
    context = {
        'mode': mode,
    }
    return render(request,'tests/test_page.html',context)


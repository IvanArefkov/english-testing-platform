from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib import messages

from .froms import CustomUserCreationForm



# Create your views here.
def loginPage (request):
    if request.user.is_authenticated:
        return redirect('home')
    page = "login"
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.warning(request, "User Does Not Exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "Login Successful")
            return redirect("home")
        else:
            messages.warning(request, 'Username or Password is incorrect!')
    context = {
        'page': page,
    }
    return render(request, 'users/login_register.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.first_name = user.first_name.lower().strip().title()
            user.last_name = user.last_name.lower().strip().title()
            user.save()
            messages.success(request, "Registration Successful")
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'An error has occurred, please try again later')
    context = {
        'page': page,
        'form': form,
    }
    return render(request,'users/login_register.html', context)
@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    messages.warning(request, 'You have been logged out.')
    return redirect('login')

@login_required(login_url='login')
def profile(request):

    return render(request, 'users/profile.html')



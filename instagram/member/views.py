from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from member.form import SignupForm, LoginForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            user.save()
        return redirect('signin')
        # return HttpResponse(f'{user.username} - {user.password}')
    else:
        form = SignupForm
        context = {
            'form': form,
        }
    return render(request, 'member/signup.html', context)


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'member/login.html', context)


def signout(request):
    logout(request)
    return redirect('signin')

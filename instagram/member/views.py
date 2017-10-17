from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from member.form import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            return HttpResponse(f'<p>{username}-{password}</p>')
        else:
            form = SignupForm()
        context = {
            'form': form,
        }
        return render(request, 'member/signup.html', context)


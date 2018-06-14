from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render


def signup(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')

        user = authenticate(username=username, password=raw_password)

        login(request, user)

        return redirect('index')

    return render(request, 'users/signup.html', {'form': form})

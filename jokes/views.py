from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .utils import get_joke

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['joke'] = get_joke()
                return redirect('joke')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Set joke in session only if it doesn't already exist
                if 'joke' not in request.session:
                    request.session['joke'] = get_joke()
                return redirect('joke')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def joke_view(request):
    if request.method == 'POST' and 'new_joke' in request.POST:
        request.session['joke'] = get_joke()
    if 'joke' not in request.session:
        request.session['joke'] = get_joke()
    joke = request.session['joke']
    return render(request, 'joke.html', {'joke': joke})

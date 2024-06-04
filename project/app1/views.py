from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from .forms import RegistrationForm, ServerForm
from django.http import HttpResponseRedirect 
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Server

@login_required
def Homepage(request):
    return render(request, 'home.html')

@never_cache
def SignupPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            my_user = User.objects.create_user(username=username, email=email, password=password)
            my_user.save()

            # Authenticate and login the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

@never_cache
def LoginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Username or password is incorrect. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def create_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            server = form.save(commit=False)
            server.owner = request.user  # Set the owner to the current user
            server.save()
            return redirect('server_created_successfully')  # Redirect to a success page
    else:
        form = ServerForm()
    return render(request, 'create_server.html', {'form': form})

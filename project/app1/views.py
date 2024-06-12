from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm, ServerForm ,ChannelForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Server, Membership ,Channel

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
    return redirect('loginn')

@login_required
def create_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            server = form.save(commit=False)
            server.owner = request.user  
            server.save()
            return redirect('server_detail', server_id=server.id)
    else:
        form = ServerForm()
    return render(request, 'create_server.html', {'form': form})


@login_required
def server_detail(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            channel = form.save(commit=False)
            channel.server = server
            channel.save()
            return redirect('server_detail', server_id=server.id)
    else:
        form = ChannelForm()
    channels = server.channels.all()  # Get all channels related to this server
    return render(request, 'server_detail.html', {'server': server, 'channels': channels, 'form': form})

@login_required
def list_servers(request):
    servers = Server.objects.filter(public=True)
    return render(request, 'list_servers.html', {'servers': servers})

@login_required
def join_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if not Membership.objects.filter(user=request.user, server=server).exists():
        Membership.objects.create(user=request.user, server=server)
    return redirect('server_detail', server_id=server.id)

@login_required
def home(request):
    user = request.user
    created_servers = Server.objects.filter(owner=user)
    joined_servers = Server.objects.filter(memberships__user=user).exclude(owner=user)
    return render(request, 'home.html', {
        'created_servers': created_servers,
        'joined_servers': joined_servers
    })


@login_required
def channel_detail(request, server_id, channel_id):
    server = get_object_or_404(Server, id=server_id)
    channel = get_object_or_404(Channel, id=channel_id, server=server)
    return render(request, 'channel_detail.html', {'server': server, 'channel': channel})
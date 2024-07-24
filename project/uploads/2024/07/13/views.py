
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm, ServerForm, ChannelForm, FriendRequestForm, SearchForm
from django.http import HttpResponseRedirect ,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Server, Membership, Channel, FriendRequest, Friendship ,Invitation ,FileUpload,Message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    search_form = SearchForm()
    search_results = []

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            username = search_form.cleaned_data['username']
            search_results = User.objects.filter(username__icontains=username).exclude(username=user.username)
            for result in search_results:
                result.already_friends = (
                    Friendship.objects.filter(user1=user, user2=result).exists() or
                    Friendship.objects.filter(user1=result, user2=user).exists() or
                    FriendRequest.objects.filter(sender=user, receiver=result, status='pending').exists() or
                    FriendRequest.objects.filter(sender=result, receiver=user, status='pending').exists()
                )

    return render(request, 'home.html', {
        'created_servers': created_servers,
        'joined_servers': joined_servers,
        'search_form': search_form,
        'search_results': search_results,
    })


@login_required
def send_friend_request(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    if receiver != request.user:
        if not FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
            if not Friendship.objects.filter(user1=request.user, user2=receiver).exists() and not Friendship.objects.filter(user1=receiver, user2=request.user).exists():
                FriendRequest.objects.create(sender=request.user, receiver=receiver)
    return redirect('home')


@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user:
        Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
        friend_request.status = 'accepted'
        friend_request.save()
    return redirect('pending_requests')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.receiver == request.user:
        friend_request.status = 'rejected'
        friend_request.save()
    return redirect('pending_requests')

@login_required
def friends_list(request):
    user = request.user
    friendships = Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)
    friends = [friendship.user1 if friendship.user2 == user else friendship.user2 for friendship in friendships]
    return render(request, 'friends_list.html', {'friends': friends})

@login_required
def pending_requests(request):
    user = request.user
    pending_requests = FriendRequest.objects.filter(receiver=user, status='pending')
    return render(request, 'pending_requests.html', {'pending_requests': pending_requests})


@login_required
def create_invitation(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if request.user != server.owner:
        return HttpResponse("You are not the owner of this server.", status=403)

    invitation = Invitation.objects.create(server=server)
    invite_link = request.build_absolute_uri(f"/invite/{invitation.code}/")

    return render(request, 'server_detail.html', {
        'server': server,
        'channels': server.channels.all(),
        'invite_link': invite_link
    })

@login_required
def join_via_invitation(request, code):
    invitation = get_object_or_404(Invitation, code=code)
    server = invitation.server
    if Membership.objects.filter(user=request.user, server=server).exists():
        return redirect('server_detail', server_id=server.id)
    return redirect('confirm_join_server', code=code)

@login_required
def confirm_join_server(request, code):
    invitation = get_object_or_404(Invitation, code=code)
    server = invitation.server
    if request.method == 'POST':
        Membership.objects.get_or_create(user=request.user, server=server)
        return redirect('server_detail', server_id=server.id)
    return render(request, 'confirm_join.html', {'server': server, 'invitation_code': code})

@login_required
def promote_to_moderator(request, server_id, user_id):
    server = get_object_or_404(Server, id=server_id)
    if request.user != server.owner:
        return redirect('server_detail', server_id=server.id)

    user = get_object_or_404(User, id=user_id)
    membership = get_object_or_404(Membership, user=user, server=server)
    membership.role = 'moderator'
    membership.save()

    return redirect('server_detail', server_id=server.id)

@login_required
def demote_to_member(request, server_id, user_id):
    server = get_object_or_404(Server, id=server_id)
    if request.user != server.owner:
        return redirect('server_detail', server_id=server.id)

    user = get_object_or_404(User, id=user_id)
    membership = get_object_or_404(Membership, user=user, server=server)
    membership.role = 'member'
    membership.save()

    return redirect('server_detail', server_id=server.id)

@login_required
def remove_member(request, server_id, user_id):
    server = get_object_or_404(Server, id=server_id)
    if request.user != server.owner and request.user.memberships.get(server=server).role != 'moderator':
        return redirect('server_detail', server_id=server.id)

    user = get_object_or_404(User, id=user_id)
    membership = get_object_or_404(Membership, user=user, server=server)
    if user != server.owner:
        membership.delete()

    return redirect('server_detail', server_id=server.id)

@login_required
def server_detail(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    memberships = server.memberships.all()
    is_moderator = Membership.objects.filter(user=request.user, server=server, role='moderator').exists()

    if request.method == 'POST' and 'name' in request.POST:
        if request.user == server.owner or is_moderator:
            channel_form = ChannelForm(request.POST)
            if channel_form.is_valid():
                channel = channel_form.save(commit=False)
                channel.server = server
                channel.save()
                return redirect('server_detail', server_id=server.id)
    else:
        channel_form = ChannelForm()

    return render(request, 'server_detail.html', {
        'server': server,
        'channels': server.channels.all(),
        'memberships': memberships,
        'owner': server.owner,
        'moderators': memberships.filter(role='moderator'),
        'channel_form': channel_form,
    })


@login_required
def channel_detail(request, server_id, channel_id):
    server = get_object_or_404(Server, id=server_id)
    channel = get_object_or_404(Channel, id=channel_id)
    messages = Message.objects.filter(channel=channel).order_by('timestamp')
    file_uploads = FileUpload.objects.filter(channel=channel).order_by('uploaded_at')

    context = {
        'server': server,
        'channel': channel,
        'messages': messages,
        'file_uploads': file_uploads,
    }
    return render(request, "channel_detail.html", context)


@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        file = request.FILES['file']
        file_instance = FileUpload.objects.create(user=request.user, channel_id=request.POST['channel_id'], file=file)
        return JsonResponse({"file_name": file_instance.file.name})
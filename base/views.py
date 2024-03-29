from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Message, Room, Topic , User
from .forms import MessageForm, MyUserCreationForm, RoomForm, UserForm, UserCreationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# login function


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            userconfirm = User.objects.get(email=email)
            login(request, userconfirm)
            print(userconfirm.email)
            return redirect("home")
        else:
            messages.error(request, "Wrong Username or Password")
    context = {"page": page}
    return render(request, "chat/login_register.html", context)


# Register


def RegisterPage(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration")
    return render(request, "chat/login_register.html", {"form": form})


# Logout function
def LogoutUser(request):
    logout(request)
    return redirect("home")


# View room


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(host__username__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_message": room_message,
    }
    return render(request, "chat/index.html", context)


# @login_required(login_url='/login')
def ProfilePage(request, pk):
    users = User.objects.get(id=pk)
    rooms = users.room_set.all()
    topics = Topic.objects.all()
    room_message = users.message_set.all()
    msgz = ""
    msg2 = ""
    for room_msgs in room_message:
        msgz = room_msgs.user.username
    for room in rooms:
        msg2 = room.host.username
    context = {
        "users": users,
        "rooms": rooms,
        "room_message": room_message,
        "msgz": msgz,
        "msg2": msg2,
        "topics": topics,
    }
    return render(request, "chat/profile.html", context)


# room with ID function


def room(request, pk):
    room = Room.objects.get(id=pk)
    referrer = request.META["HTTP_REFERER"]
    room_messages = (
        room.message_set.all()
    )  # _set.all() is used for One-to-many relationship
    participants = (
        room.participants.all()
    )  # .all() is used for Many-To-Many relationship
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)
    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "chat/room.html", context)


# Create room route here


@login_required(login_url="/login")
def CreateRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        # if form.is_valid():
        #    room=  form.save(commit=False)
        #    room.host=request.user
        #    room.save()
        return redirect("home")
    context = {"form": form, "topics": topics}
    return render(request, "chat/room_form.html", context)


# Update room here
@login_required(login_url="/login")
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    page_update = "update"
    if request.user == room.host or request.user.is_superuser == True:
        if request.method == "POST":
            topic_name = request.POST.get("topic")
            topic, created = Topic.objects.get_or_create(name=topic_name)
            room.name = request.POST.get("name")
            room.topic = topic
            room.description = request.POST.get("description")
            room.save()
            return redirect("home")
        context = {
            "form": form,
            "topics": topics,
            "room": room,
            "page_update": page_update,
        }
        return render(request, "chat/room_form.html", context)
    referrer = request.META["HTTP_REFERER"]
    messages.error(request, "Sorry, You are not permited to updated this room")
    print(referrer)
    return HttpResponseRedirect(referrer)

    # if request.user != room.host:
    #      referrer = request.META['HTTP_REFERER']
    #      messages.error(request, 'Sorry, You are not permited to updated this room')
    #      print(referrer)
    #      return HttpResponseRedirect(referrer)
    # if request.method == 'POST':
    #     form = RoomForm(request.POST, instance=room)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')
    # context ={'form':form}
    # return render(request, 'chat/room_form.html', context)


# Delete view
@login_required(login_url="/login")
def DeleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user == room.host or request.user.is_superuser == True:
        if request.method == "POST":
            room.delete()
            return redirect("home")
        return render(request, "chat/delete.html", {"obj": room})
    referrer = request.META["HTTP_REFERER"]
    messages.error(request, "Sorry, You are not permited to delete this room")
    print(referrer)
    return HttpResponseRedirect(referrer)

    # if request.user != room.host:
    #     referrer = request.META['HTTP_REFERER']
    #     messages.error(request, 'Sorry, You are not permited to delete this room')
    #     print(referrer)
    #     return HttpResponseRedirect(referrer)
    # if request.user.is_superuser == True:
    #     if request.method == 'POST':
    #         room.delete()
    #         return redirect ('home')
    # return render (request, 'chat/delete.html', {'obj': room})


# Delete message
@login_required(login_url="/login")
def DeleteMessage(request, pk):
    room_message = Message.objects.get(id=pk)
    if request.method == "POST":
        if request.user == room_message.user or request.user.is_superuser == True:
            print(request.user)
            room_message.delete()
            messages.success(request, "Message deleted successfully")
            print(request.user.is_superuser)
            return redirect("home")
        else:
            referrer = request.META["HTTP_REFERER"]
            messages.error(
                request, "Sorry, You are not permited to delete this message"
            )
            print(referrer)
            return HttpResponseRedirect(referrer)
    return render(request, "chat/delete.html", {"obj": room_message})


# Update room message here
@login_required(login_url="/login")
def UpdateMessage(request, pk):
    msg_update = Message.objects.get(id=pk)
    form = MessageForm(instance=msg_update)
    if request.user != msg_update.user:
        referrer = request.META["HTTP_REFERER"]
        messages.error(request, "Sorry, You are not permited to updated this message")
        print(referrer)
        return HttpResponseRedirect(referrer)
    if request.method == "POST":
        form = MessageForm(request.POST, instance=msg_update)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "chat/room_form.html", context)


@login_required(login_url="/login")
def UpdateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile-page", pk=user.id)
    return render(request, "chat/update-user.html", {"form": form})


def TopicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "chat/topics.html", {"topics": topics})


def ActivityPage(request):
    room_messages = Message.objects.all()
    return render(request, "chat/activity.html", {"room_messages": room_messages})


# rooms = [
#     {'id':1, 'name': 'Lets learn python'},
#      {'id':2, 'name': 'Lets learn Java'},
#      { 'id':3, 'name': 'Lets learn C#'},
#        {'id':4, 'name': 'Design with me'},
#        ]


# def home(request):
#     context ={'rooms':rooms}
#     return render (request, 'chat/index.html',context)

# def room(request, pk):
#     room = None
#     for i in rooms:
#         if i['id'] == int(pk):
#             room =i
#             context = {'room': room}

#     return render (request, 'chat/room.html', context)

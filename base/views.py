from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import Message, Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import  User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm

# login function

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            userconfirm = User.objects.get(username=username)
            login(request, userconfirm)
            print(userconfirm.email)
            return redirect ('home')
        else:
            messages.error(request, 'Wrong Username or Password')
    context = {'page': page}
    return render (request, 'chat/login_register.html', context)


# Register

def RegisterPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit =False)
            # if User.objects.get(username = user.username):
            #     messages.error(request, 'Username already exist')
            #     print('Username already exist')
            user.username =user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'chat/login_register.html', {'form': form})


# Logout function
def LogoutUser(request):
    logout(request)
    return redirect ('home')

# View room

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q)
        
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context ={'rooms':rooms,  'topics': topics, 'room_count' : room_count}
    return render (request, 'chat/index.html',context)




def room(request, pk):
    room = Room.objects.get(id =pk)
    room_messages = room.message_set.all().order_by('-created') #_set.all() is used for One-to-many relationship
    participants = room.participants.all() #.all() is used for Many-To-Many relationship
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants' : participants}
    return render (request, 'chat/room.html', context)



# Create room route here

@login_required(login_url='/login')
def CreateRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form =RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'chat/room_form.html', context)


# Update room here
@login_required(login_url='/login')
def UpdateRoom(request, pk):
    room =Room.objects.get(id=pk)
    form =RoomForm(instance=room)
    if request.user != room.host:
         referrer = request.META['HTTP_REFERER']
         messages.error(request, 'Sorry, You are not permited to updated this room')
         print(referrer)
         return HttpResponseRedirect(referrer)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid(): 
            form.save()
            return redirect('home')
    context ={'form':form}
    return render(request, 'chat/room_form.html', context)





# Delete view
@login_required(login_url='/login')
def DeleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        referrer = request.META['HTTP_REFERER']
        messages.error(request, 'Sorry, You are not permited to delete this room')
        print(referrer)
        return HttpResponseRedirect(referrer)
    if request.method == 'POST':
        room.delete()
        return redirect ('home')
    return render (request, 'chat/delete.html', {'obj': room})








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
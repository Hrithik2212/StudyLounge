from django.shortcuts import render , redirect 
from .models import Room , Topic , User
from django.contrib import  messages
from django.contrib.auth import authenticate , login ,  logout 
from .forms import RoomForm
from django.db.models import Q
# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("User-Name")
        password = request.POST.get("password")

        try :
            user = User.objects.get(username=username)
        except:
            messages.error(request , "User doesn't exist")

        user = authenticate(request , username=username , password=password)

        if user is not None :
            login(request , user )
            return redirect('home')
        else :
            messages.error(request , "The password you have enetered is incorrect ")

    return render(request , 'base/login_registration.html')

def logout_page(request):
    logout(request)
    return render(request , 'base/login_registration.html')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(names__icontains=q) |
        Q(description__icontains=q)) # .get() , .filter() , .exclude()
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms , 'topics' : topics , 'room_count':room_count} 
    return render(request ,'base/home.html', context  ) # pass in the context dictionary 

def room(request , pk ):
    rooms = Room.objects.get(id=pk) 
    context = {'room' : rooms}
    return render(request , 'base/room.html' ,context )


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context  = {'form':form} 
    return render(request , 'base/room_form.html', context )

def update_room(request , pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    context = {'form':form}
    if request.method == 'POST':
        form = RoomForm(request.POST , instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request , 'base/room_form.html' , context ) 

def delete_room(request , pk ):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request , 'base/delete.html' , {'obj':room} )
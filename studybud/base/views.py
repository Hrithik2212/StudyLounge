from django.shortcuts import render , redirect 
from django.http import HttpResponse
from .models import *
from django.contrib import  messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login ,  logout 
from .forms import RoomForm , UserForm
from django.db.models import Q
# Create your views here.


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get("User-Name")
        password = request.POST.get("password")

        try :
            user = User.objects.get(username=username)
        except:
            messages.error(request , "User doesn't exist")

        if request.user.is_authenticated:
            return redirect('home')
        
        user = authenticate(request , username=username , password=password)

        if user is not None :
            login(request , user )
            return redirect('home')
        else :
            messages.error(request , "The password you have entered is incorrect ")
        
    context = {'page' : page }

    return render(request , 'base/login_registration.html' , context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = UserCreationForm()
    # context = {'page' : page , 'form':form }
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid() :
            user_name = request.POST.get('username')
            password = request.POST.get('password')
            try : 
                User.objects.get(user_name= user_name)
                messages.error(request ,"Username aldready exists")
            except: 
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request , user)
                return redirect('home')
        else : 
            messages.error(request , 'An error occured during registration')
    
    context = {'page' : page , 'form':form }
    return render(request , 'base/login_registration.html' , context)

# def registerUser(request):
#     print('Register got triggered')
#     page = 'register'
#     context = {'page':page}
#     if request.method == 'POST' : 
#         # print('Post works ')
#         username = request.POST.get('User-Name')
#         password= request.POST.get('password')
#         repassword = request.POST.get('repassword')
#         if password != repassword :
#             messages.error(request , 'The passwords you have entered dose not match')

#         else :    
#             try:
#                 User.objects.get(username=username)
#                 messages.error(request , 'The username aldready exists')
#             except :
#                 # print('Except block')
#                 user_form = UserForm(request.POST)
#                 print(user_form.errors)
                
#                 if user_form.is_valid():
#                     print('if worked')
#                     form=user_form.save(commit=False)
#                     form.save()
#                     return redirect('login')
            

#     return render(request , 'base/login_registration.html' , context )

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(names__icontains=q) |
        Q(description__icontains=q)) # .get() , .filter() , .exclude()
    topics = Topic.objects.all() 
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms ,
                'topics' : topics ,
                  'room_count':room_count , 
                  'room_messages' : room_messages} 
    return render(request ,'base/home.html', context  ) # pass in the context dictionary 

def room(request , pk ):
    room = Room.objects.get(id=pk) 
    messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    if request.method == 'POST' :
        message =  Message.objects.create(
            user = request.user , 
            room = room , 
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room' , pk=room.id )
    no_of_particpants = participants.count()
    context = {'room' : room , 
               'messages':messages , 
               'participants':participants ,
               'participant_count':no_of_particpants}
    return render(request , 'base/room.html' ,context )


@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context  = {'form':form} 
    return render(request , 'base/room_form.html', context )

@login_required(login_url='/login')
def update_room(request , pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host :
        return HttpResponse("This room is not built by you , so you can't delete it ")
    context = {'form':form}
    if request.method == 'POST':
        form = RoomForm(request.POST , instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request , 'base/room_form.html' , context ) 

@login_required(login_url='/login')
def delete_room(request , pk ):
    room = Room.objects.get(id=pk)
    if request.user != room.host :
        return HttpResponse("This room is not built by you , so you can't delete it ")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request , 'base/delete.html' , {'obj':room} )


@login_required(login_url='/login')
def delete_message(request , pk ):
    message = Message.objects.get(id=pk)
    if request.user != message.user :
        return HttpResponse("You are not allowed to delete this message")
    if request.method == 'POST':
        message.delete()
        return redirect(f'home')
    return render(request , 'base/delete.html' , {'obj': message} )

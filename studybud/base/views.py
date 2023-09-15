from django.shortcuts import render
from .models import Room 

# Create your views here.
def home(request):
    rooms = Room.objects.all() # .get() , .filter() , .exclude()
    context = {'rooms': rooms} 
    return render(request ,'base/home.html', context  ) # pass in the context dictionary 

def room(request , pk ):
    rooms = Room.objects.get(id=pk) 
    context = {'room' : rooms}
    return render(request , 'base/room.html' ,context )





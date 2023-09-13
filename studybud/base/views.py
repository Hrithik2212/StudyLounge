from django.shortcuts import render
from .models import Room 


rooms =  [ 
     {'id':1 , 'names' : "Python"} , 
     {'id':2 , 'names' : 'Java'} , 
     {'id':3 , 'names' : 'C++'} 
]
# Create your views here.
def home(request):
    rooms = Room.objects.all() # .get() , .filter() , .exclude()
    context = {'rooms': rooms} 
    return render(request ,'base/home.html', context  ) # pass in the context dictionary 

def room(request , pk ):
    room = Room.objects.all() 
    for i in rooms:
        if i['id'] == int(pk) :
            room  = i 
    context = {'room' : room}
    return render(request , 'base/room.html' ,context )





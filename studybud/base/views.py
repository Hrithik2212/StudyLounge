from django.shortcuts import render

rooms =  [ 
     {'id':1 , 'names' : "Python"} , 
     {'id':2 , 'names' : 'Java'} , 
     {'id':3 , 'names' : 'C++'} 
]
# Create your views here.
def home(request):
    context = {'rooms': rooms} 
    return render(request ,'base/home.html', context  ) # pass in the context dictionary 

def room(request , pk ):
    room = None 
    for i in rooms:
        if i['id'] == int(pk) :
            room  = i 
    context = {'room' : room}
    return render(request , 'base/room.html' ,context )





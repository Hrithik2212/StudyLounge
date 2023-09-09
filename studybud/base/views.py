from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path 

rooms =  [ 
     {'id':1 , 'names' : "Python"} , 
     {'id':2 , 'names' : 'Java'} , 
     {'id':3 , 'names' : 'C++'} 
]
# Create your views here.
def home(request):
    context = {'rooms': rooms} 
    return render(request ,'home.html', context  ) # pass in the context dictionary 

def room(request):
    return render(request , 'Room.html' )





from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
    # A topic can have multiple room 
    # A room can have only one topic 
    name = models.CharField(max_length=200)

class Room(models.Model):
    host = models.ForeignKey(User , on_delete=models.SET_NULL ,null=True)
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL,null=True)
    names = models.CharField(max_length=200)
    description = models.TextField(null=True , blank= True)
    # participants = None 
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True )

    def __str__(self):
        return self.names


class Message(models.Model):
    user =  models.ForeignKey(User ,on_delete=models.CASCADE )
    room = models.ForeignKey(Room , on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
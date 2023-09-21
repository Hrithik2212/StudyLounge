from django.forms import ModelForm
from .models import Room , User

class RoomForm(ModelForm):
    class Meta:
        model = Room 
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User 
        fields = ['username' , 'password']
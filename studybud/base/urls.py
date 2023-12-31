from django.urls import path
from . import views 

urlpatterns  = [ 
        path('' , views.home , name="home" ) , 
        path('rooms/<str:pk>/',views.room , name="room") , 
        path('create-room/', views.create_room , name="create-room"),
        path('update-room/<str:pk>/' , views.update_room , name ="update-room"),
        path('delete-room/<str:pk>/' , views.delete_room , name ="delete-room"),
        path('login/' , views.login_page , name="login") , 
        path('logout/' , views.logoutUser , name='logout'),
        path('register/' , views.registerUser , name="register") , 
        path('delete-message/<str:pk>/' , views.delete_message , name ="delete-message"),
        path('user-profile/<str:pk>/' , views.userProfile , name="user-profile") ,
]
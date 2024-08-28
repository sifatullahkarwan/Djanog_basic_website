from django.urls import path
from . import views

urlpatterns=[

    path('login/',views.loginpage,name ='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),


    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),# :pk let us to give id number for our same page
    path('profile/<str:pk>/',views.userprofile,name = 'usre-profile'),


    path('create-room/',views.creatRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name = 'update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage,name = 'delete-message'),
 

]
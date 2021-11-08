from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.RegisterPage, name='register'),
    path('logout/', views.LogoutUser, name='logout'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.CreateRoom, name="create-room"),
    path('update-room/<str:pk>/', views.UpdateRoom, name="update-room"),
    path('Delete-room/<str:pk>/', views.DeleteRoom, name="delete-room")


]
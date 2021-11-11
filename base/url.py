from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.RegisterPage, name='register'),
    path('logout/', views.LogoutUser, name='logout'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.ProfilePage, name='profile-page'),
    path('create-room/', views.CreateRoom, name="create-room"),
    path('update-room/<str:pk>/', views.UpdateRoom, name="update-room"),
    path('update-message/<str:pk>/', views.UpdateMessage, name="update-message"),
    path('update-user/', views.UpdateUser, name="update-user"),
    path('Delete-room/<str:pk>/', views.DeleteRoom, name="delete-room"),
    path('Delete-message/<str:pk>/', views.DeleteMessage, name="delete-message"),
    path('topics', views.TopicsPage, name="topics"),
    path('activity', views.ActivityPage, name="activity")



]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('success/', views.success, name='success'),
]
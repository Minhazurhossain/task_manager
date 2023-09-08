from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('task/', views.task, name='task'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('get_task/', views.get_task, name='get_task'),
]
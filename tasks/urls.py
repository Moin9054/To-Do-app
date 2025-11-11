from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.list_tasks, name='list'),
    path('create/', views.create_task, name='create'),
    path('edit/<int:pk>/', views.edit_task, name='edit'),
    path('delete/<int:pk>/', views.delete_task, name='delete'),
    path('toggle/<int:pk>/', views.toggle_task, name='toggle'),
]

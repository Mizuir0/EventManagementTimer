from django.urls import path
from .views import pomodoro_timer, add, delete, edit

urlpatterns = [
    path('', pomodoro_timer, name='pomodoro_timer'),
    path('add/', add, name="add"),
    path('delete/', delete, name="delete"),
    path('edit/<int:timer_id>/', edit, name="edit"),
]
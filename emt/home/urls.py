from django.urls import path
from .views import pomodoro_timer, add, delete

urlpatterns = [
    path('', pomodoro_timer, name='pomodoro_timer'),
    path('add/', add, name="add"),
    path('delete/', delete, name="delete"),
]
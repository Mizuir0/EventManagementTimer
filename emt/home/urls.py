from django.urls import path
from .views import pomodoro_timer, add, delete, edit, reorder

urlpatterns = [
    path('', pomodoro_timer, name='pomodoro_timer'),
    path('add/', add, name="add"),
    path('delete/<int:timer_id>/', delete, name="delete"),
    path('edit/<int:timer_id>/', edit, name="edit"),
    path('reorder/', reorder, name="reorder"),
]
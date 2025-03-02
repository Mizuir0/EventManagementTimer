from django.shortcuts import render, redirect
from .models import Timers
from .forms import PomodoroForm
from django.db.models import Sum, F, ExpressionWrapper, fields

# views.py

def pomodoro_timer(request):
  first_timer = Timers.objects.first()
  timers = Timers.objects.all()
  form = PomodoroForm()
  
  if len(timers) == 0:
      return render(request, 'pomodromo_timer.html', {
          'form': form,
          'editable': False,
          'timers': None,
      })
  
  return render(request, 'pomodromo_timer.html', {
      'form': form,
      'editable': False,
      'timers': timers,
      'first_timer': first_timer,
  })

def add(request):
    editable = True
    if request.method == "POST":
        editable = False
        form = PomodoroForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            # form_instance.uuid = id
            form_instance.save()
            return redirect("pomodoro_timer")
    else:
        form = PomodoroForm()
        timers = Timers.objects.all()
        return render(request, 'pomodromo_timer.html', {
            'form': form,
            "editable": editable,
            'timers': timers
        })


def delete(request):
    timers = Timers.objects.all()
    timers.delete()
    print("Successfully Deleted")
    form = PomodoroForm()
    return render(request, 'pomodromo_timer.html', {
        'form': form,
        "editable": False,
        'timers': None
    })
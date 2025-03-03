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
    editable = "add"
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
    
def edit(request, timer_id):
    editable = "edit"
    timer = Timers.objects.get(id=timer_id)
    
    if request.method == "POST":
        editable = False
        form = PomodoroForm(request.POST, instance=timer)
        if form.is_valid():
            form.save()
            return redirect("pomodoro_timer")
    else:
        form = PomodoroForm(instance=timer)
        timers = Timers.objects.all()
        return render(request, 'pomodromo_timer.html', {
            'form': form,
            "editable": editable,
            'timers': timers,
            'timer': timer
        })

def delete(request, timer_id):
    timer = Timers.objects.get(id=timer_id)
    timer.delete()
    print("Successfully Deleted")
    return redirect("pomodoro_timer")
    # timers = Timers.objects.all()
    # form = PomodoroForm()
    # if len(timers) == 0:
    #     return render(request, 'pomodromo_timer.html', {
    #         'form': form,
    #         "editable": False,
    #         'timers': None
    #     })
    # return render(request, 'pomodromo_timer.html', {
    #     'form': form,
    #     "editable": False,
    #     'timers': timers
    # })
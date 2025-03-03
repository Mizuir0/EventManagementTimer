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
    timers = Timers.objects.all().order_by('id')
    
    # 一時的に uuid フィールドに現在の順序を保存
    for i, t in enumerate(timers, 1):
        t.uuid = i
        t.save(update_fields=['uuid'])
    
    # Auto Increment キーをリセット (MySQL/MariaDBの場合)
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("ALTER TABLE home_timers AUTO_INCREMENT = 1")
    
    # 新しいIDでタイマーを作り直す
    for t in timers:
        old_id = t.id
        # 一度削除
        t.delete()
        
        # 新しいタイマーを作成（同じデータで）
        new_timer = Timers(
            band_name=t.band_name,
            minutes=t.minutes,
            item1=t.item1,
            item2=t.item2,
            item3=t.item3,
            uuid=t.uuid
        )
        new_timer.save()
    
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
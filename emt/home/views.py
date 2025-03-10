from django.shortcuts import render, redirect
from .models import Timers
from .forms import PomodoroForm
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.http import JsonResponse
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import connection, transaction

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
    
    # SQLiteではAUTO_INCREMENTをリセットする直接的な方法はないため、
    # sqlite_sequence テーブルを直接操作する
    with connection.cursor() as cursor:
        # sqlite_sequenceテーブルが存在するか確認（初めての場合は存在しない可能性がある）
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
        if cursor.fetchone():
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'home_timers'")
    
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

@ensure_csrf_cookie
def reorder(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data sent by the client
            data = json.loads(request.body)
            timer_order = data.get('timer_order', [])
            
            if not timer_order:
                return JsonResponse({'success': False, 'error': 'No timer order provided'})
            
            with transaction.atomic():
                # Similar approach to the delete method
                # Get all timers and store their data temporarily
                timers_data = []
                for timer_id in timer_order:
                    try:
                        timer = Timers.objects.get(id=timer_id)
                        timers_data.append({
                            'band_name': timer.band_name,
                            'minutes': timer.minutes,
                            'item1': timer.item1,
                            'item2': timer.item2,
                            'item3': timer.item3,
                            'uuid': timer.uuid
                        })
                    except Timers.DoesNotExist:
                        return JsonResponse({'success': False, 'error': f'Timer with ID {timer_id} not found'})
                
                # Delete all timers
                Timers.objects.all().delete()
                
                # Reset auto increment for SQLite
                with connection.cursor() as cursor:
                    # sqlite_sequenceテーブルが存在するか確認
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence'")
                    if cursor.fetchone():
                        cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'home_timers'")
                
                # Create new timers in the specified order
                for data in timers_data:
                    new_timer = Timers(**data)
                    new_timer.save()
                
                return JsonResponse({'success': True})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Activity, HabitProgress, PomodoroStats, TodoStats, Note, Task
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def landing_page(request):
    return render(request, 'index.html')

def habit_view(request):
    if request.method == 'POST':
        habit_name = request.POST.get('habit_name')
        completed = request.POST.get('completed') == 'true'
        
        # Record habit activity
        activity = Activity(
            activity_type='habit',
            details='{}'  # Initialize with empty JSON string
        )
        activity.set_details({'habit_name': habit_name, 'completed': completed})
        activity.save()
        
        # Update habit progress
        HabitProgress.objects.create(
            habit_name=habit_name,
            completed=completed,
            streak_count=1 if completed else 0
        )
    
    return render(request, 'habit.html')

@login_required
def todo_view(request):
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"User: {request.user}")
    print(f"User ID: {request.user.id}")
    print(f"Request method: {request.method}")
    print(f"Request headers: {dict(request.headers)}")
    print(f"Request cookies: {request.COOKIES}")
    
    if request.method == 'POST':
        try:
            print(f"Raw request body: {request.body}")
            data = json.loads(request.body)
            action = data.get('action')
            print(f"POST request received. Action: {action}")
            print(f"POST data: {data}")
            
            if not request.user.is_authenticated:
                print("User not authenticated")
                return JsonResponse({'error': 'User not authenticated'}, status=401)
            
            if action == 'add':
                text = data.get('text')
                if not text:
                    print("Error: Task text is required")
                    return JsonResponse({'error': 'Task text is required'}, status=400)
                    
                try:
                    task = Task.objects.create(
                        user=request.user,
                        text=text,
                        priority=data.get('priority', 'normal')
                    )
                    print(f"Task created: {task}")
                    print(f"Task user: {task.user}")
                    print(f"Task user ID: {task.user.id}")
                    
                    response_data = {
                        'id': task.id,
                        'text': task.text,
                        'completed': task.completed,
                        'createdAt': task.created_at.isoformat(),
                        'priority': task.priority
                    }
                    print(f"Sending response: {response_data}")
                    return JsonResponse(response_data)
                except Exception as e:
                    print(f"Error creating task: {e}")
                    return JsonResponse({'error': str(e)}, status=500)
                
            elif action == 'complete':
                task_id = data.get('task_id')
                try:
                    task = Task.objects.get(id=task_id, user=request.user)
                    task.completed = not task.completed
                    task.save()
                    print(f"Task toggled: {task}")
                    
                    # Record activity
                    activity = Activity.objects.create(
                        user=request.user,
                        activity_type='todo',
                        details={
                            'action': 'complete' if task.completed else 'uncomplete',
                            'task_id': task.id,
                            'task_text': task.text
                        }
                    )
                    
                    # Update stats
                    stats, _ = TodoStats.objects.get_or_create(user=request.user)
                    if task.completed:
                        stats.completed_tasks += 1
                        if task.priority == 'high':
                            stats.priority_tasks_completed += 1
                    else:
                        stats.completed_tasks = max(0, stats.completed_tasks - 1)
                        if task.priority == 'high':
                            stats.priority_tasks_completed = max(0, stats.priority_tasks_completed - 1)
                    stats.save()
                    
                    return JsonResponse({'success': True})
                except Task.DoesNotExist:
                    print(f"Task not found: {task_id}")
                    return JsonResponse({'error': 'Task not found'}, status=404)
                except Exception as e:
                    print(f"Error toggling task: {e}")
                    return JsonResponse({'error': str(e)}, status=500)
                    
            elif action == 'delete':
                task_id = data.get('task_id')
                try:
                    task = Task.objects.get(id=task_id, user=request.user)
                    task.delete()
                    print(f"Task deleted: {task_id}")
                    return JsonResponse({'success': True})
                except Task.DoesNotExist:
                    print(f"Task not found for deletion: {task_id}")
                    return JsonResponse({'error': 'Task not found'}, status=404)
                except Exception as e:
                    print(f"Error deleting task: {e}")
                    return JsonResponse({'error': str(e)}, status=500)
            else:
                print(f"Invalid action: {action}")
                return JsonResponse({'error': 'Invalid action'}, status=400)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Request body: {request.body}")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    # GET request - return all tasks
    try:
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')
        print(f"Found {tasks.count()} tasks for user {request.user}")
        tasks_data = [{
            'id': task.id,
            'text': task.text,
            'completed': task.completed,
            'createdAt': task.created_at.isoformat(),
            'priority': task.priority
        } for task in tasks]
        
        print(f"Returning {len(tasks_data)} tasks")
        print(f"Tasks data: {tasks_data}")
        return render(request, 'todo.html', {
            'tasks_json': json.dumps(tasks_data)
        })
    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def pomodoro_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'complete':
            duration = int(request.POST.get('duration', 25))
            task = request.POST.get('task', '')
            
            # Record pomodoro activity
            activity = Activity(
                activity_type='pomodoro',
                duration=duration,
                details='{}'  # Initialize with empty JSON string
            )
            activity.set_details({'task': task})
            activity.save()
            
            # Update pomodoro stats
            today = timezone.now().date()
            stats, _ = PomodoroStats.objects.get_or_create(date=today)
            stats.total_sessions += 1
            stats.total_focus_time += duration
            if task:
                stats.completed_tasks += 1
            stats.save()
    
    return render(request, 'pomodoro.html')

@login_required
def notes_view(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        
        if not name or not desc:
            return JsonResponse({
                'status': 'error',
                'message': 'Please fill in all fields'
            })
        
        note = Note.objects.create(
            user=request.user,
            name=name,
            desc=desc
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Note saved successfully!',
            'note': {
                'id': note.id,
                'name': note.name,
                'desc': note.desc,
                'date': note.date.strftime("%B %d, %Y, %I:%M %p")
            }
        })
    
    notes = Note.objects.filter(user=request.user).order_by('-date')
    return render(request, 'notes.html', {'notes': notes})

@login_required
@require_POST
def delete_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
        note.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Note deleted successfully!'
        })
    except Note.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Note not found!'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

def relax_view(request):
    if request.method == 'POST':
        activity_type = request.POST.get('activity_type')
        duration = int(request.POST.get('duration', 0))
        
        # Record relaxation activity
        activity = Activity(
            activity_type='relax',
            duration=duration,
            details='{}'  # Initialize with empty JSON string
        )
        activity.set_details({'activity_type': activity_type})
        activity.save()
    
    return render(request, 'relax.html')

def bubble_view(request):
    return render(request, 'bubble.html')

def spacegame_view(request):
    return render(request, 'spacegame.html')

def tictac_view(request):
    return render(request, 'tictac.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Username validation
        if len(username) < 3:
            messages.error(request, "Username must be at least 3 characters long!")
            return redirect('Hello:signup')
        
        if not re.match("^[a-zA-Z0-9_]+$", username):
            messages.error(request, "Username can only contain letters, numbers, and underscores!")
            return redirect('Hello:signup')

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address!")
            return redirect('Hello:signup')

        # Password validation
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long!")
            return redirect('Hello:signup')
        
        if not re.search(r'[A-Z]', password1):
            messages.error(request, "Password must contain at least one uppercase letter!")
            return redirect('Hello:signup')
        
        if not re.search(r'[a-z]', password1):
            messages.error(request, "Password must contain at least one lowercase letter!")
            return redirect('Hello:signup')
        
        if not re.search(r'[0-9]', password1):
            messages.error(request, "Password must contain at least one number!")
            return redirect('Hello:signup')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            messages.error(request, "Password must contain at least one special character!")
            return redirect('Hello:signup')

        if password1 != password2:
            messages.error(request, "Passwords don't match!")
            return redirect('Hello:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('Hello:signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('Hello:signup')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to ZEN-ORBIT!")
            return redirect('Hello:notes')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('Hello:signup')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if not username or not password:
            messages.error(request, "Please fill in all fields!")
            return redirect('Hello:login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if not remember_me:
                # Set session expiry to 0 to close the browser when it's closed
                request.session.set_expiry(0)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('Hello:notes')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('Hello:login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('Hello:home')

# (Optional) A dummy logout view (e.g. def logout_view(request): ...) can be added later if needed.
from django.shortcuts import render
from datetime import datetime
from home.models import Notes
from django.contrib import messages
from django.shortcuts import HttpResponse,redirect
from django.http import JsonResponse
import json
import nltk  # noqa: F401
from nltk.corpus import stopwords  # noqa: F401


# Create your views here.
def index(request):
    context = {
        "variable1":"Harry is great",
        "variable2":"Rohan is great"
    } 
    return render(request, 'index.html', context)
    # return HttpResponse("this is homepage")

def todo(request):
    return render(request, 'todo.html') 

def pomo(request):
    return render(request, 'pomo.html')
 

def notes(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            
            if not name or not desc:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fill in both title and content.'
                })
                
            note = Notes(name=name, desc=desc)
            note.save()
            
            # If it's an AJAX request, return the new note data
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'note': {
                        'id': note.id,
                        'name': note.name,
                        'desc': note.desc,
                        'date': note.date.strftime("%B %d, %Y, %I:%M %p")
                    }
                })
            
            messages.success(request, 'Your note has been saved successfully!')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                })
            messages.error(request, f'Error saving note: {str(e)}')
    
    # Get all notes ordered by date (newest first)
    notes_list = Notes.objects.all().order_by('-date')
    
    context = {
        'notes': notes_list,
        'debug': True
    }
    return render(request, 'notes.html', context)

def delete_note(request, note_id):
    if request.method == "POST":
        try:
            note = Notes.objects.get(id=note_id)
            note.delete()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Note deleted successfully!'
                })
            messages.success(request, 'Note deleted successfully!')
        except Notes.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Note not found!'
                })
            messages.error(request, 'Note not found!')
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                })
            messages.error(request, f'Error deleting note: {str(e)}')
    return redirect('notes')
 
def habit(request):
    return render(request, 'habit.html')

def relax(request):
    return render(request, 'relax.html')

def bubble(request):
    return render(request, 'bubble.html')

def tictac(request):
    return render(request, 'tictac.html')

def spacegame(request):
    return render(request, 'space.html')


from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def todo(request):
    return render(request, 'todo.html')

def pomo(request):
    return render(request, 'pomo.html')

def notes(request):
    return render(request, 'notes.html')

def relax(request):
    return render(request, 'relax.html')

def habit(request):
    return render(request, 'habit.html')

def bubble(request):
    return render(request, 'bubble.html')

def tictactoe(request):
    return render(request, 'tictactoe.html')


from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='home'),  # Map the root URL to the index view
    path('todo', views.todo, name='todo'),
    path('pomo', views.pomo, name='pomo'),
    path('notes', views.notes, name='notes'),
    path('habit', views.habit, name='habit'),
    path('relax', views.relax, name='relax'),
    path('bubble', views.bubble, name='bubble'),
    path('tictac', views.tictac, name='tictac'),
]

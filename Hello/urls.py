from django.urls import path
from . import views

app_name = 'Hello'

urlpatterns = [
    # Landing page
    path('', views.landing_page, name='home'),
    
    # Feature routes
    path('habit/', views.habit_view, name='habit'),
    path('todo/', views.todo_view, name='todo'),
    path('pomodoro/', views.pomodoro_view, name='pomodoro'),
    path('notes/', views.notes_view, name='notes'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('relax/', views.relax_view, name='relax'),
    path('bubble/', views.bubble_view, name='bubble'),
    path('spacegame/', views.spacegame_view, name='spacegame'),
    path('tictac/', views.tictac_view, name='tictac'),
    
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

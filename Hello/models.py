from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(default=0)
    details = models.TextField(default='{}')

    def set_details(self, details_dict):
        self.details = json.dumps(details_dict)

    def get_details(self):
        return json.loads(self.details)

class HabitProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    habit_name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)
    streak_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Habit Progress'

class PomodoroStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    total_sessions = models.IntegerField(default=0)
    total_focus_time = models.IntegerField(default=0)
    completed_tasks = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Pomodoro Stats'

class TodoStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    completed_tasks = models.IntegerField(default=0)
    priority_tasks_completed = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Todo Stats'

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, default='normal', choices=[
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High')
    ])

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.text} ({self.user.username})"

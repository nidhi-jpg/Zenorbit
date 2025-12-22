from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Note, Task

# Register the Note model
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date')
    list_filter = ('user', 'date')
    search_fields = ('name', 'desc')
    ordering = ('-date',)

# Register the Task model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'completed', 'priority', 'created_at')
    list_filter = ('completed', 'priority', 'user')
    search_fields = ('text',)
    ordering = ('-created_at',)

# Customize the User admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site
admin.site.site_header = "ZENORBIT Admin"
admin.site.site_title = "ZENORBIT Admin Portal"
admin.site.index_title = "Welcome to ZENORBIT Admin" 
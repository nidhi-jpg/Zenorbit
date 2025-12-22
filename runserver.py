#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hello.settings')
django.setup()

# Increase recursion limit
sys.setrecursionlimit(10000)

if __name__ == '__main__':
    execute_from_command_line(['manage.py', 'runserver', '--noreload']) 
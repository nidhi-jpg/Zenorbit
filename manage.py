#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Increase recursion limit to handle inspect module issues
sys.setrecursionlimit(10000)

def main():
    """Run administrative tasks."""
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myauthproject.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

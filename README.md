# Zenorbit - Django Project

A Django web application project with authentication and various features.

## Features

- User authentication system
- Todo management
- Habit tracking
- Pomodoro timer
- Notes functionality
- Relaxation tools
- Mini games (Bubble, Tic-tac-toe)

## Setup

### Requirements

- Python 3.8+
- Django 3.2.25

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

## Render Deployment

This repository includes `render.yaml`, so it can be deployed as a Render Blueprint.

- Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start command: `gunicorn myauthproject.wsgi:application`
- Python version: `python-3.11.9`

Required environment variables are defined in `render.yaml`. Render will generate `SECRET_KEY`; `DEBUG` should stay `False` in production.

## Project Structure

- `Hello/` - Main application
- `myauthproject/` - Authentication project settings
- `userproject/` - User-related functionality
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)

## Technologies Used

- Django 3.2.25
- Python
- HTML/CSS
- JavaScript


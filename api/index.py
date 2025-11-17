"""
Vercel serverless function entry point for Django application
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Import Django
import django
django.setup()

# Import WSGI application
from myproject.wsgi import application

# Vercel expects the WSGI application to be named 'app'
app = application


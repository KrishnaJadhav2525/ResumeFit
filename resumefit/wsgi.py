"""
WSGI config for resumefit project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resumefit.settings')
application = get_wsgi_application()

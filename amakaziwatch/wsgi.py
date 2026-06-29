"""
WSGI config for amakaziwatch project.
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Add apps directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amakaziwatch.settings')

application = get_wsgi_application()

"""
ASGI config for restaurant_admin project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_admin.settings')

application = get_asgi_application()






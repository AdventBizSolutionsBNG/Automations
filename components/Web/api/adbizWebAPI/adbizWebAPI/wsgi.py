"""
WSGI config for adbizWebAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""
import sys
import os
sys.path.append('/home/setupadmin/adbiz/components/Web/api/adbizWebAPI')
sys.path.append('/home/setupadmin/adbiz/components/Web/api/adbizWebAPI/adbizWebAPI')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adbizWebAPI.settings')

application = get_wsgi_application()

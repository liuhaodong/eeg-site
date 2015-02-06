"""
WSGI config for EEG project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

from EEG.debug.views import dump
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EEG.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

from django.core.wsgi import get_wsgi_application
#from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()

'''
print 'started dump'
dump(None)
print 'done dump'
'''

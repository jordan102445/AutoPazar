import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

from api.wsgi import app

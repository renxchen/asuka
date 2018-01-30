import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(sys.path[0])))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apolo_server.processor.db_units.settings")
django.setup()
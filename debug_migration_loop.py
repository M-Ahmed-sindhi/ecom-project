import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectname.settings')
django.setup()

from django.apps import apps
from django.contrib.contenttypes.models import ContentType

print("Iterating over all models...")
for app_config in apps.get_app_configs():
    print(f"Checking app: {app_config.label}")
    for klass in app_config.get_models():
        print(f"  Checking model: {klass.__name__}")
        try:
            ctype = ContentType.objects.get_for_model(klass)
            print(f"    ContentType ID: {ctype.id}")
            h = hash(ctype)
            print(f"    Hash: {h}")
        except Exception as e:
            print(f"    ERROR for {klass.__name__}: {e}")

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectname.settings')
django.setup()

from django.contrib.auth.models import User

try:
    if not User.objects.filter(username='testadmin').exists():
        User.objects.create_superuser('testadmin', 'admin@example.com', 'password123')
        print("Superuser 'testadmin' created successfully!")
    else:
        print("Superuser 'testadmin' already exists.")
except Exception as e:
    print(f"Failed to create user: {e}")

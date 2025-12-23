import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectname.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

try:
    print("Creating/Getting ContentType for User...")
    ct = ContentType.objects.get_for_model(User)
    print(f"ContentType: {ct}")
    print(f"ID: {ct.id}")
    print(f"PK: {ct.pk}")
    print(f"Hash: {hash(ct)}")
    
    print("Creating/Getting ContentType for Permission...")
    from django.contrib.auth.models import Permission
    ct_perm = ContentType.objects.get_for_model(Permission)
    print(f"ContentType: {ct_perm}")
    print(f"ID: {ct_perm.id}")
    
except Exception as e:
    print(f"Error: {e}")

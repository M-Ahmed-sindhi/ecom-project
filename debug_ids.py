import os
import django
import pymongo
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectname.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# 1. Inspect Raw DB
load_dotenv()
client = pymongo.MongoClient(os.getenv("MONGO_HOST"))
db = client['Clusters0']
collection = db['django_content_type']

print("--- RAW MONGODB ---")
raw_user_ct = collection.find_one({"model": "user", "app_label": "auth"})
print(f"User ContentType (Raw): {raw_user_ct}")
if raw_user_ct:
    print(f"ID Type: {type(raw_user_ct.get('_id'))}")

# 2. Inspect ORM
print("\n--- DJANGO ORM ---")
try:
    ct = ContentType.objects.get(app_label='auth', model='user')
    print(f"User ContentType (ORM): {ct}")
    print(f"ID: {ct.id} (Type: {type(ct.id)})")
    print(f"PK: {ct.pk} (Type: {type(ct.pk)})")
except Exception as e:
    print(f"Error fetching via ORM: {e}")

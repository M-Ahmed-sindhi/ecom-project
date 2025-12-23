import os
import django
import pymongo
from dotenv import load_dotenv

# 1. Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectname.settings')
django.setup()

from django.apps import apps
from django.conf import settings

# 2. Setup PyMongo
load_dotenv()
mongo_host = os.getenv("MONGO_HOST")
print(f"Connecting to MongoDB: {mongo_host}")

client = pymongo.MongoClient(mongo_host)
db_name = 'Clusters0' # Match settings.py
db = client[db_name]
collection = db['django_content_type']

# 3. Iterate and Bootstrap
print("Bootstrapping ContentTypes...")
count = 0

for app_config in apps.get_app_configs():
    for klass in app_config.get_models():
        # Calculate exactly what Django *would* store
        opts = klass._meta
        app_label = opts.app_label
        model_name = opts.model_name
        
        # Check if exists raw
        existing = collection.find_one({
            "app_label": app_label,
            "model": model_name
        })
        
        if existing:
            print(f"  [OK] {app_label}.{model_name} exists")
        else:
            print(f"  [MISSING] {app_label}.{model_name} - INSERTING NOW")
            # Generate an integer ID (hash or simple increment if valid)
            # Use a high number or random safe int, or simple increment if collection empty
            # For simplicity, and since we dropped it, we can use simple increment
            # But safer to maybe use a hash of the name to be deterministic?
            # Let's use simple counter + large offset to avoid collisions if any exist
            
            # Simple integer ID strategy
            import zlib
            crc = zlib.crc32(f"{app_label}.{model_name}".encode())
            
            result = collection.insert_one({
                "_id": crc, # FORCE INTEGER ID
                "id": crc,  # FORCE EXPLICIT ID field for Djongo?
                "app_label": app_label,
                "model": model_name
            })
            print(f"    -> Created with INT ID: {crc}")
            count += 1

print(f"Done! Bootstrapped {count} missing ContentTypes.")
print("Now run: python3 manage.py migrate")

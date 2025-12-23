import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

mongo_host = os.getenv("MONGO_HOST")
print(f"Connecting to: {mongo_host}")

try:
    client = pymongo.MongoClient(mongo_host)
    db = client['Clusters0']
    
    # Check if collection exists
    if 'django_migrations' not in db.list_collection_names():
        db.create_collection('django_migrations')
        print("Created 'django_migrations' collection successfully!")
    else:
        print("'django_migrations' already exists.")
        
except Exception as e:
    print(f"Error: {e}")

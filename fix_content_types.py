import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

mongo_host = os.getenv("MONGO_HOST")
print(f"Connecting to: {mongo_host}")

try:
    client = pymongo.MongoClient(mongo_host)
    db_name = 'Clusters0' # Match settings.py
    db = client[db_name]
    
    collections_to_drop = ['django_content_type', 'auth_permission']
    
    for collection_name in collections_to_drop:
        if collection_name in db.list_collection_names():
            print(f"Found collection '{collection_name}'. Dropping it...")
            db.drop_collection(collection_name)
            print(f"Collection '{collection_name}' dropped successfully.")
        else:
            print(f"Collection '{collection_name}' does not exist.")
        
    print("Please run 'python3 manage.py migrate' now.")
        
except Exception as e:
    print(f"Error: {e}")

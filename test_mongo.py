import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

mongo_host = os.getenv("MONGO_HOST")
print(f"Connecting to: {mongo_host}")

try:
    client = pymongo.MongoClient(mongo_host)
    # Force connection checking
    client.admin.command('ping')
    print("Ping successful!")
    
    db = client['Clusters0']
    collection = db['test_connection']
    result = collection.insert_one({"message": "Hello Railway!"}) # Try to write
    print(f"Insert successful! ID: {result.inserted_id}")
    
    # Clean up
    collection.delete_one({"_id": result.inserted_id})
    print("Delete successful!")
    
except Exception as e:
    print(f"Connection failed: {e}")

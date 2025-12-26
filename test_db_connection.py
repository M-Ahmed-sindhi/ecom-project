
import pymongo
import sys
import dns.resolver

# Connection string provided by user
URI = "mongodb+srv://admin:shaikh@cluster0.gojn0ly.mongodb.net/?retryWrites=true&w=majority"

try:
    print(f"Attempting to connect to: {URI}")
    client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=5000)
    # Trigger a connection
    info = client.server_info()
    print("SUCCESS: Connected to MongoDB!")
    print(f"Server version: {info.get('version')}")
except Exception as e:
    print(f"FAILURE: Could not connect to MongoDB.")
    print(f"Error: {e}")
    sys.exit(1)

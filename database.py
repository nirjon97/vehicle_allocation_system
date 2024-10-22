from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection
client = None
db =None

def connect_db():
    global client, db  # Ensure we're modifying the global variables
    
    # MongoDB connection URI
    uri = "mongodb+srv://nirjonsarker97:FLjnQP0f9qHRSIg5@nirjondb.8wlry.mongodb.net/?retryWrites=true&w=majority&appName=nirjondb"
    
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Set the database (replace 'nirjondb' with your actual database name)
        db = client["nirjondb"]  # Now 'db' will be globally accessible
        
        # Print to confirm successful connection
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        db = None  # Set db to None in case of failure



def prepopulate_vehicles_and_employees():
    vehicles_collection = db.vehicles
    employees_collection = db.employees

    # Only populate if collection is empty
    if vehicles_collection.count_documents({}) == 0:
        vehicles_data = []
        for i in range(1, 1001):
            vehicles_data.append({
                "vehicle_id": f"V{i:03d}",
                "model": f"Model-{i}",
                "driver": {
                    "driver_id": f"D{i:03d}",
                    "name": f"Driver {i}",
                    "license_number": f"LIC-{i:03d}"
                }
            })
        vehicles_collection.insert_many(vehicles_data)

    if employees_collection.count_documents({}) == 0:
        employees_data = []
        for i in range(1, 1001):
            employees_data.append({
                "employee_id": f"E{i:03d}",
                "name": f"Employee {i}",
                "department": f"Department-{(i % 10) + 1}"
            })
        employees_collection.insert_many(employees_data)

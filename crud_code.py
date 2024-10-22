from datetime import datetime,date
from fastapi import HTTPException
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from database import db  # Import the global 'db' object from the database module

# Allocation CRUD operations
uri = "mongodb+srv://nirjonsarker97:FLjnQP0f9qHRSIg5@nirjondb.8wlry.mongodb.net/?retryWrites=true&w=majority&appName=nirjondb"
client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Set the database (replace 'nirjondb' with your actual database name)
db = client["nirjondb"]  # Now 'db' will be globally accessible
print("db is here now....",db)



def create_allocation(data):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    collection = db.allocations
    
    # Access the 'date' field
    allocation_date = data["date"]  

    # Convert to datetime.datetime if allocation_date is a string
    if isinstance(allocation_date, str):
        allocation_date = datetime.strptime(allocation_date, "%Y-%m-%d")
    elif isinstance(allocation_date, date):  # Check if it's already a date object
        # Convert to datetime.datetime at midnight (start of the day)
        allocation_date = datetime.combine(allocation_date, datetime.min.time())

    # Check if the vehicle is already allocated for this date
    existing_allocation = collection.find_one({
        "vehicle_id": data["vehicle_id"],
        "date": allocation_date
    })

    if existing_allocation:
        raise HTTPException(status_code=400, detail="Vehicle is already allocated for this date.")

    allocation = {
        "employee_id": data["employee_id"],
        "vehicle_id": data["vehicle_id"],
        "date": allocation_date  # Store as datetime object
    }
    
    result = collection.insert_one(allocation)
    return str(result.inserted_id)


def update_allocation(allocation_id, update_data):
    collection = db.allocations
    
    # Find the allocation by allocation_id
    allocation = collection.find_one({"_id": ObjectId(allocation_id)})
    
    if not allocation:
        raise Exception("Allocation not found")
    
    # Retrieve the allocation date
    allocation_date = allocation.get("date")  # Use .get() to avoid KeyError
    
    # Check if allocation_date is None
    if allocation_date is None:
        return {"error": "Allocation date is not set."}

    # Ensure allocation_date is a datetime object for comparison
    if isinstance(allocation_date, datetime):
        allocation_date = allocation_date.date()  # Convert to date for comparison

    # Compare to the current date
    if allocation_date <= datetime.now().date():
        return {"error": "Allocation can only be updated before the allocation date."}

    # Update only fields that were provided
    if "employee_name" in update_data:
        # Implement logic to update the employee based on their name if needed
        employee_name = update_data.pop("employee_name")
        # Check if employee exists and update accordingly

    collection.update_one({"_id": ObjectId(allocation_id)}, {"$set": update_data})
    return {"message": "Allocation updated successfully."}



def delete_allocation(allocation_id):
    collection = db.allocations
    allocation = collection.find_one({"_id": ObjectId(allocation_id)})

    if not allocation:
        return {"error": "Allocation not found."}

    # Ensure the date field exists and is not None before comparing
    allocation_date = allocation.get("date")

    if allocation_date is None:
        return {"error": "Allocation date is missing or invalid."}

    # If allocation_date is a datetime object, convert it to a date object
    if isinstance(allocation_date, datetime):
        allocation_date = allocation_date.date()

    # Compare the allocation date with the current date
    if allocation_date <= datetime.now().date():
        return {"error": "Allocation can only be deleted before the allocation date."}

    collection.delete_one({"_id": ObjectId(allocation_id)})
    return {"message": "Allocation deleted successfully."}





def get_allocation_history(filters):
    collection = db.allocations
    query = {}

    if filters.get("employee_id"):
        query["employee_id"] = filters["employee_id"]
    if filters.get("vehicle_id"):
        query["vehicle_id"] = filters["vehicle_id"]
    

    # Fetch allocations
    allocations = list(collection.find(query))

    # Convert ObjectId to string for each allocation
    for allocation in allocations:
        allocation["_id"] = str(allocation["_id"])

    return allocations

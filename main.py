from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
from routers import vehicle
from datetime import date
from crud_code import get_allocation_history  # Import the function from crud_code
from pydantic import BaseModel
from database import connect_db, prepopulate_vehicles_and_employees

app = FastAPI()

# Connect to the database on startup
@app.on_event("startup")
def startup_db():
    connect_db()  # Ensure the database connection is initialized
    prepopulate_vehicles_and_employees()

# Include the vehicle router for API endpoints
app.include_router(vehicle.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Vehicle Allocation System"}


#for filter
class AllocationHistoryFilter(BaseModel):
    employee_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    

@app.get("/allocation/history", response_model=List[dict])
def get_allocation_history_route(
    employee_id: Optional[str] = Query(None),
    vehicle_id: Optional[str] = Query(None),
    
):
    # Prepare the filter parameters into a dictionary
    filters = {
        "employee_id": employee_id,
        "vehicle_id": vehicle_id,
        
    }

    # Fetch allocation history using the get_allocation_history function from crud_code
    try:
        allocation_history = get_allocation_history(filters)
        if not allocation_history:
            raise HTTPException(status_code=404, detail="No allocations found")
        return allocation_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


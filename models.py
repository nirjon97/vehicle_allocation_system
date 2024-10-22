from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class Driver(BaseModel):
    driver_id: str
    name: str
    license_number: str

class Vehicle(BaseModel):
    vehicle_id: str
    model: str
    driver: Driver

class Employee(BaseModel):
    employee_id: str
    name: str
    department: str

class AllocationCreate(BaseModel):
    employee_id: str
    vehicle_id: str
    date: date

class AllocationUpdate(BaseModel):
    vehicle_id: Optional[str] = None
    date: Optional[date] = None
    
class AllocationResponse(BaseModel):
    id: str = Field(..., alias="_id")
    employee_id: str
    vehicle_id: str
    date: date
    driver: Driver

class AllocationHistoryFilter(BaseModel):
    employee_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    driver_id: Optional[str] = None

   

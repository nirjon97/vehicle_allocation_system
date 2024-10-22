from fastapi import APIRouter, HTTPException
from models import AllocationCreate, AllocationUpdate, AllocationResponse, AllocationHistoryFilter
from crud_code import create_allocation, update_allocation, delete_allocation, get_allocation_history
from typing import List

router = APIRouter()

@router.post("/allocate", response_model=str)
def allocate_vehicle(allocation: AllocationCreate):
    allocation_data = allocation.dict()
    result = create_allocation(allocation_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.put("/allocate/{allocation_id}", response_model=dict)
def update_vehicle_allocation(allocation_id: str, update_data: AllocationUpdate):
    result = update_allocation(allocation_id, update_data.dict(exclude_unset=True))
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.delete("/allocate/{allocation_id}", response_model=dict)
def delete_vehicle_allocation(allocation_id: str):
    result = delete_allocation(allocation_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result



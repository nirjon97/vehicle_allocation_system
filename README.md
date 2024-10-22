#Vehicle Allocation System

Project Overview :

The Vehicle Allocation System is a web application built with FastAPI and MongoDB to manage the allocation of vehicles to employees within an organization. The system allows employees to allocate vehicles for a specific date, ensuring that no vehicle is double-allocated on the same day.

Features :
Allocate vehicles to employees for specific dates. Prevent double allocation of vehicles on the same day. Update and delete vehicle allocations. Fetch allocation history with filtering options.

Architecture :
Backend: FastAPI Database: MongoDB

Getting Started :
To set up the project locally, follow these steps:

Clone the repository:

git clone
cd vehicle_allocation_system

Create a virtual environment :

python -m venv env source env/bin/activate

Install dependencies :
"pip install fastapi uvicorn pymongo"

Set up MongoDB: Ensure you have MongoDB installed and running. You can set up a local instance or use a cloud provider like MongoDB Atlas.

Run the application:

uvicorn main:app --reload
The application will be available at http://127.0.0.1:8000/docs.

API Endpoints:

Allocation Endpoints :
Create Allocation :
Endpoint: POST /allocate

Update Allocation :
Endpoint: PUT /allocate/{allocation_id}

Delete Allocation :
Endpoint: DELETE /allocate/{allocation_id}

Get Allocation History :
Endpoint: GET /allocation/history

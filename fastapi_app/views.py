# fastapi_app/views.py

from fastapi import APIRouter, HTTPException, Depends
from .schemas import TaskRequest, TaskResponse
from tasks.models import Task 
from django.contrib.auth import get_user_model
from .celery_utils import trigger_task_async  #
from .tasks import process_task

router = APIRouter()

@router.post("/tasks/", response_model=TaskResponse)
async def create_task(request_data: TaskRequest):
    User = get_user_model()
    try:
        user = User.objects.first()  
        raise HTTPException(status_code=500, detail="No user found.")

    task = Task.objects.create(
        title=request_data.title,
        description=request_data.description,
        status="PENDING",
        created_by=user
    )

    trigger_task_async(task.id)

    return TaskResponse(task_id=task.id, message="Task submitted for processing.")
import httpx
from fastapi import APIRouter
from fastapi.responses import JSONResponse

@router.get("/graphql/tasks/")
async def fetch_tasks_from_graphql():
    query = """
    {
        tasks {
            id
            title
            status
            createdBy {
                id
                username
            }
        }
    }
    """
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/graphql/", json={"query": query})
        return JSONResponse(response.json())
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from .security import get_current_user

app = FastAPI()

@app.get("/secure-data/")
async def secure_endpoint(current_user=Depends(get_current_user)):
    return JSONResponse({
        "message": "Access granted!",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        }
    })

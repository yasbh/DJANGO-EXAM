from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import httpx
import os
from transformers import pipeline
from typing import Optional


# Create FastAPI app
app = FastAPI()

# CORS middleware (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Django settings from environment
DJANGO_API_BASE = os.getenv("DJANGO_API_BASE", "http://localhost:8000/api")
DJANGO_GRAPHQL_URL = os.getenv("DJANGO_GRAPHQL_URL", "http://localhost:8000/graphql/")

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



VERIFY_TOKEN_URL = f"{DJANGO_API_BASE}/auth/verify_token/"

async def validate_token(token: str = Depends(oauth2_scheme)):
    headers = {"Authorization": f"Token {token}"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(VERIFY_TOKEN_URL, headers=headers, timeout=5)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token"
                )
            user_data = response.json()
            return user_data
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )



class TaskCreateRequest(BaseModel):
    input_data: str
    token: str  

@app.get("/")
async def root():
    return {"message": "FastAPI app is running"}

@app.post("/tasks/")
async def create_task(
    request_data: TaskCreateRequest,
    user_data: dict = Depends(validate_token)  # Protect endpoint with token validation
):
    """
    Create a task in Django by calling Django DRF endpoint.
    """
    headers = {"Authorization": f"Token {request_data.token}"}
    data = {"input_data": request_data.input_data}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{DJANGO_API_BASE}/tasks/",
                headers=headers,
                json=data,
                timeout=10
            )
            if response.status_code == 201:
                return {"message": "Task created successfully", "data": response.json()}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with Django: {str(e)}")
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

@app.patch("/api/tasks/{task_id}")
async def patch_task(task_id: int, task_update: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.dict(exclude_unset=True)
    tasks[task_id].update(update_data)
    return tasks[task_id]


@app.delete("/api/tasks/{task_id}/")
async def delete_task(task_id: int):
    return {"detail": "Task deleted successfully"}

@app.get("/results/")
async def get_results(
    token: str,
    user_data: dict = Depends(validate_token)  
):
    
    headers = {"Authorization": f"Token {token}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{DJANGO_API_BASE}/results/",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                return {"results": response.json()}
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Error communicating with Django: {str(e)}")

@app.post("/graphql/")
async def graphql_proxy(request: Request, user_data: dict = Depends(validate_token)):
    
    body = await request.json()
    headers = {}
    auth = request.headers.get("Authorization")
    if auth:
        headers["Authorization"] = auth

    async with httpx.AsyncClient() as client:
        response = await client.post(DJANGO_GRAPHQL_URL, json=body, headers=headers)
        response.raise_for_status()
        return JSONResponse(content=response.json())
class PredictRequest(BaseModel):
    input_data: str

model = pipeline("sentiment-analysis")

@app.post("/predict/")
async def predict(request_data: PredictRequest):
    input_text = request_data.input_data
    result = model(input_text)
    return {"prediction": result}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred", "details": str(exc)},
    )

## Building High-Performance APIs with FastAPI and Django

A comprehensive full-stack project that integrates **Django**, **FastAPI**, **Celery**, **GraphQL**, and **AI-based prediction** into a unified, high-performance API. The project features shared data models, robust real-time data ingestion, background task processing, GraphQL APIs, and secure authentication using OAuth2.

>  **Project supervised by Mr. Chaouki Bayoudhi**

## Stack

- **Backend Frameworks**: Django, FastAPI
- **API Formats**: REST, GraphQL
- **Serialization & Validation**: Django REST Framework, Pydantic, Graphene-Django
- **Background Tasks**: Celery + Redis
- **Authentication**: OAuth2 + Django Token Auth

# DJANGO-EXAM

## Project Objectives

The system was built to showcase modern Python web development techniques including:
- Building and validating relational data models.
- Creating secure REST APIs using Django REST Framework.
- Executing background tasks using Celery and Redis.
- Implementing FastAPI for high-speed real-time services.
- Securing APIs with OAuth2 and Django tokens.
- Integrating GraphQL to allow flexible data access.
- Simulating AI predictions using mock logic.
- Designing a modular and integrated architecture.


##  Technologies Used

| Tech              | Purpose                                 |
|-------------------|-----------------------------------------|
| Django            | Core backend & REST API                 |
| DRF (REST)        | Serializers, ViewSets, Authentication   |
| Celery + Redis    | Background task queue                   |
| FastAPI           | Real-time APIs + AI simulation          |
| Graphene-Django   | GraphQL query engine                    |
| Pydantic          | FastAPI request validation              |
| JWT + OAuth2      | Authentication & authorization          |

##  What I Did

- Defined `Task` and `Result` models with constraints and foreign key relationships.
- Registered models in Django Admin with filters and search.
- Created DRF serializers for request validation.
- Implemented RESTful endpoints to create and retrieve tasks/results.
- Used Django TokenAuthentication and JWT for user login and security.
- Configured Celery to process submitted tasks asynchronously.
- Simulated AI processing (predictions with confidence) in Celery worker.
- Created FastAPI endpoints for:
  - Submitting tasks
  - Getting task details
  - Generating AI predictions
- Used Pydantic to validate FastAPI request schemas.
- Built GraphQL types and resolvers to fetch tasks and results via GraphQL API.
- Enabled OAuth2 + token security for FastAPI routes.

## How to Run It

1. Install dependencies
   pip install -r requirements.txt

2. redis-server

3. python manage.py makemigrations
python manage.py migrate

4. celery -A core worker --loglevel=info
5. python manage.py runserver
6. uvicorn fastapi_app.main:app --reload --port 8001

## most important functions in your project
1. process_task(task_id) – Celery Task (Background Worker)
 File: tasks/tasks.py
Role: Asynchronously processes a task submitted by the user.

What It Does:
Updates task status to "STARTED".

Simulates a 5-second processing delay.

Generates mock output (like an AI result).

Creates a Result linked to the task.

Marks the task as "SUCCESS" or "FAILURE" if an error occurs.

2. create_task() – FastAPI Task Submission Endpoint
file :fastapi_app/views.py
Role: Submits a task to Django from FastAPI and triggers Celery.

What It Does:
Accepts a TaskRequest from the user.

Creates a task in the Django backend.

Uses trigger_task_async() to start background processing.

Returns task ID and success message

3. predict() – AI Prediction Simulation (FastAPI)
File: fastapi_app/main.py
Role: Simulates an AI model that returns a prediction.

What It Does:
Accepts user input (text).

Randomly generates a prediction label and confidence.

Returns the mock prediction

4. get_current_user() – Token Authentication for FastAPI
File: fastapi_app/security.py
Role: Validates Django Token inside FastAPI routes.

What It Does:
Extracts token from Authorization header.

Checks the token in Django’s DB.

Returns the linked user or throws error if invalid.

5.  trigger_task_async(task_id) – Celery Helper
 File: fastapi_app/celery_utils.py
Role: Allows FastAPI to trigger a Celery task.

6. schema.py – GraphQL Resolvers
File: tasks/schema.py
Role: Defines queries for GraphQL API.

Examples:
resolve_tasks() → returns all tasks

resolve_results() → returns all results

7. VerifyTokenView – Token Validation API (DRF)
 File: tasks/views.py
Role: Checks if a token is valid (used by FastAPI).

# fastapi_app/celery_utils.py

from tasks.tasks import process_task  

def trigger_task_async(task_id):
    process_task.delay(task_id)  

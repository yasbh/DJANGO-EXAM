# tasks/tasks.py

import time
from celery import shared_task
from .models import Task, Result
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_task(task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.status = 'STARTED'
        task.save()

        # Simulate long-running task
        time.sleep(5)
        output = {"prediction": "some_result", "confidence": 0.95}

        Result.objects.create(task=task, output=output)
        task.status = 'SUCCESS'
        task.save()
        return f"Task {task_id} processed."

    except Task.DoesNotExist:
        logger.error(f"Task {task_id} not found.")
        return f"Task {task_id} not found."

    except Exception as e:
        logger.exception(f"Task {task_id} failed.")
        if 'task' in locals():
            task.status = 'FAILURE'
            task.save()
            Result.objects.create(task=task, output={}, errors=str(e))
        return f"Task {task_id} failed: {str(e)}"

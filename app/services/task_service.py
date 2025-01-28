from app import db
from app.models.task import Task

"""Create Task"""

def create_task(title: str, description: str, user_id: int) -> Task:
    task = Task(title=title, description=description, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return task

"""Delete Task"""

def delete_task(task_id: int) -> bool:
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        return True 
    return False

"""Update Task"""

def update_task(task_id: int, title: str = None, description: str = None) -> Task:
    task = Task.query.get(task_id)
    if title:
        task.title = title
    if description:
        task.description = description
    db.session.commit()
    return task

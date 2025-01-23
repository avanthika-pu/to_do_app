from app import db
from app.models.task import Task

def create_task(title: str, description: str, user_id: int) -> bool:
    task = Task(title=title, description=description, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return True

def delete_task(task_id: int) -> bool:
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        return True 
    else:
        return False

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
    else:
        return False
    
"""Archive task"""

def archive_task_service(task_id: int) -> bool:
    try:
        result = Task.query.filter_by(id=task_id).update({'archived': True})
        if result:
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error archiving task: {e}")
        return False
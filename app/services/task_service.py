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
    return False
    
"""update task"""

def update_task(task_id: int, title: str = None, description: str = None) -> bool:
    try:
        updated_values = {key: value for key, value in {'title': title, 'description': description}.items() if value}
        if updated_values:
            Task.query.filter_by(id=task_id).update(updated_values)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False

"""List all tasks"""

def get_all_tasks():
    tasks = Task.query.all() 
    return tasks

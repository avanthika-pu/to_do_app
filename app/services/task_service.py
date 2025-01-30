from app import db
from app.models.task import Task
from app.models.users import User


def create_task(title: str, description: str, user_id: int) -> bool:
    """Create Task"""
    try:
        if not User.query.get(user_id):
            raise ValueError(f"User with ID {user_id} does not exist.")
        task = Task(title=title, description=description, user_id=user_id)
        db.session.add(task)
        db.session.commit()
        return True
    except ValueError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        print(f"An unexpected error occurred: {e}")
        return False


def delete_task(task_id: int) -> bool:
    """Delete Task"""
    try:
         task_deleted = Task.query.filter_by(id=task_id).delete()
         if task_deleted:
            db.session.commit()
            return True
         return False
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        return False
    

def archive_task_service(task_id: int) -> bool:
    """Archive Task"""
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
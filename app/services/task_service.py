from app import db
from app.models.task import Task
from flask import g
from typing import Dict



def create_task(data: Dict) -> bool:
    """Create Task"""
    try:
        print(data['title']) 
        task = Task(title=data['title'], description=data['description'], user_id= g.user['id'])
        db.session.add(task)
        db.session.commit()
        return task
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return False



def delete_task(task_id: int) -> bool:
    """Delete Task"""
    try:
        result = Task.query.filter_by(id=task_id).delete()
        if result:
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error:{e}")
        return False                                                                       
    
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


def archive_task(task_id: int) -> bool:
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

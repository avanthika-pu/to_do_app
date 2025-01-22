from app import db
from app.models.task import Task

def create_task(title, description, user_id):
    task = Task(title=title, description=description, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return task
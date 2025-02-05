from flask import (request, jsonify, Blueprint)

from app import db
from app.models.task import Task
<<<<<<< HEAD
from app.services.task_service import (
    create_task, delete_task, get_all_tasks)
=======
from app.services.task_service import (create_task, delete_task, archive_task_service)
>>>>>>> origin/main


task_blueprint = Blueprint('task', __name__)

<<<<<<< HEAD
@task_blueprint.route('/', methods=['POST'])
=======
@task_blueprint.route('/tasks', methods=['POST'])
>>>>>>> origin/main
def create_task():
    """Create Task"""
    create_task(request.json) 
    return jsonify({"message": "Successfully created task", "status": 201})


<<<<<<< HEAD

@task_blueprint.route('/<int:task_id>', methods=['DELETE'])
=======
@task_blueprint.route('/task/delete_task/<int:task_id>', methods=['DELETE'])
>>>>>>> origin/main
def delete_task_route(task_id):
    """Delete Task"""
    success = delete_task(task_id)
    if success:
        return jsonify({"message": "Task successfully deleted", "status": 200})
    return jsonify({"message": "Task not found or failed to delete", "status": 404})

#archive task
@task_blueprint.route('/archive/<int:task_id>', methods=['PUT'])
def archive_task_route(task_id):
    success = archive_task_service(task_id)
    if success:
        return jsonify({"message": "Task archived successfully", "status": 200})
    return jsonify({"message": "Task not found", "status": 404})
    

<<<<<<< HEAD

@task_blueprint.route('/update/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    """Update Task"""
    data = request.json
    task = Task.query.get(task_id)
    task.title = data.get('title', task.title)
    task.decription = data.get('description', task.description)
    db.session.commit()
    return jsonify({"message": "Task updated successfully", "status": 200})


@task_blueprint.route('/task', methods = ['GET'])
def get_task():
    """List all Tasks"""
    tasks = get_all_tasks()  
    tasks_list = [{"id": task.id, "title": task.title, "description": task.description, "user_id": task.user_id} for task in tasks]
    return jsonify({"tasks": tasks_list, "status": 200})
=======
>>>>>>> origin/main

from flask import (request, jsonify, Blueprint)

from app import db
from app.models.task import Task
from app.services.task_service import (create_task, delete_task, get_all_tasks)


task_blueprint = Blueprint('task', __name__)


#Create Task

@task_blueprint.route('/create', methods=['POST'])
def create_task_route():
    create_task(request.json)
    return jsonify({"message": "Successfully created task", "status": 201})

@task_blueprint.route('/task', methods=['POST'])
def create_task():
    create_task(request.json) 
    return jsonify({"message": "Successfully created user", "status": 201})

#delete task 

@task_blueprint.route('/<int:task_id>', methods=['DELETE'])
@task_blueprint.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    success = delete_task(task_id)
    if success:
        return jsonify({"message": "Task successfully deleted", "status": 200})
    return jsonify({"message": "Task not found", "status": 404})

#update task

@task_blueprint.route('/update/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    task.title = data.get('title', task.title)
    task.decription = data.get('description', task.description)
    db.session.commit()
    return jsonify({"message": "Task updated successfully", "status": 200})

#List tasks
@task_blueprint.route('/task', methods = ['GET'])
def get_all_task_route():
    tasks = get_all_tasks()  
    tasks_list = [{"id": task.id, "title": task.title, "description": task.description, "user_id": task.user_id} for task in tasks]
    return jsonify({"tasks": tasks_list, "status": 200})
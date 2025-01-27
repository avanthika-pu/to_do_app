from flask import (request, jsonify, Blueprint)
from app import db
from app.models.task import Task
from app.services.task_service import create_task, delete_task, archive_task_service


task_blueprint = Blueprint('task', __name__)

@task_blueprint.route('/tasks', methods=['POST'])
def create_task():
    create_task(request.json) 

    return jsonify({"message": "Successfully created user", "status": 200}), 200

#delete task 

@task_blueprint.route('/task/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    success = delete_task(task_id)

    if success:
        return jsonify({"message": "Task successfully deleted", "status": 200}), 200
    else:
        return jsonify({"message": "Task not found or failed to delete", "status": 404}), 404

#archive task
@task_blueprint.route('/archive_task/<int:task_id>', methods=['PUT'])
def archive_task_route(task_id):
    success = archive_task_service(task_id)
    if success:
        return jsonify({"message": "Task archived successfully", "status": 200}), 200
    else:
        return jsonify({"message": "Task not found", "status": 404}), 404
    


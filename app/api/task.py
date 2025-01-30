from flask import (request, jsonify, Blueprint)

from app import db
from app.models.task import Task
from app.services.task_service import (create_task, delete_task, archive_task_service)


task_blueprint = Blueprint('task', __name__)

@task_blueprint.route('/', methods=['POST'])
def create_task():
    create_task(request.json) 
    return jsonify({"message": "Successfully created task", "status": 201})



@task_blueprint.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    success = delete_task(task_id)
    if success:
        return jsonify({"message": "Task successfully deleted", "status": 200})
    return jsonify({"message": "Task not found or failed to delete", "status": 404})


@task_blueprint.route('/archive/<int:task_id>', methods=['PUT'])
def archive_task_route(task_id):
    success = archive_task_service(task_id)
    if success:
        return jsonify({"message": "Task archived successfully", "status": 200})
    return jsonify({"message": "Task not found", "status": 404})
    


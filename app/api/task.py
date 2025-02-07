from flask import (request, jsonify, Blueprint, g)

from app import db
from app.models.task import Task
from .auth import tokenAuth
from app.services.auth import AuthService
from app.services.custom_errors import NoContent
from app.services.task_service import (
    create_task, update_task,delete_task, archive_task )

auth_service = AuthService()

task_blueprint = Blueprint('task', __name__)


@task_blueprint.route('/', methods=['POST'])
@tokenAuth.login_required()
def creating_task():
    """Create Task"""
    task = create_task(request.json) 
    if task:
        return jsonify({"message": "Successfully created task", "status": 201})
    return jsonify({"message":"Failed to create task", "status":404})


@task_blueprint.route('/<int:task_id>', methods=['DELETE'])
@tokenAuth.login_required()
def deleting_task(task_id):
    """Delete Task"""
    success = delete_task(task_id)
    if success:
        return jsonify({"message": "Task successfully deleted", "status": 200})
    return jsonify({"message": "Task not found or failed to delete", "status": 404})


@task_blueprint.route('/<int:task_id>', methods=['PUT'])
@tokenAuth.login_required()
def updating_task(task_id):
    """Update Task"""
    data = request.json
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"message": "Task not found", "status": 404})
    updated = update_task(task_id, data.get("title"), data.get("description"))

    if updated:
        return jsonify({"message": "Task successfully updated", "status": 200})
    return jsonify({"message": "Failed to update task", "status": 400}), 400


@task_blueprint.route('/archive/<int:task_id>', methods=['PUT'])
@tokenAuth.login_required()
def archiving_task(task_id):
    success = archive_task(task_id)
    if success:
        return jsonify({"message": "Task archived successfully", "status": 200})
    return jsonify({"message": "Task not found", "status": 404})
    

@task_blueprint.route('/', methods = ['GET'])
@tokenAuth.login_required
def get_task():
    """List all Tasks"""
    print(g.user)
    tasks = Task.query.filter_by(user_id=g.user['id'], is_deleted=False).paginate(
    page=int(request.args.get('page', 1)),
    per_page=int(request.args.get('page', 10))
)

    data = [task.to_dict() for task in tasks.items]
    if data:
        return jsonify({'data': data,'pagination': {'total': tasks.total,'current_page': tasks.page,'per_page': tasks.per_page,'length': len(data)},
            'message': 'Success','status': 200})
    
    raise NoContent()
from flask import (request, jsonify, Blueprint)

from app import db
from app.models.task import Task
from app.services.task_service import (create_task, delete_task)


task_blueprint = Blueprint('task', __name__)


#Create Task

@task_blueprint.route('/create', methods=['POST'])
def create_task_route():
    create_task(request.json)
    return jsonify({"message": "Successfully created task", "status": 201})


#delete task 

@task_blueprint.route('/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    success = delete_task(task_id)
    if success:
        return jsonify({"message": "Task successfully deleted", "status": 200})
    return False

#update task
@task_blueprint.route('/update/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    task.title = data.get('title', task.title)
    task.decription = data.get('description', task.description)
    db.session.commit()
    return jsonify({"message": "Task updated successfully", "status": 200})
    



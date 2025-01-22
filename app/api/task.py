from flask import request, jsonify, Blueprint
from app import db
from app.models.task import Task


task_blueprint = Blueprint('task', __name__)

@task_blueprint.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data['title']
    description = data['description']
    user_id = data['user_id']

    task = Task(title=title, description=description,user_id=user_id)
    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Successfully created task", "status": 200}), 200

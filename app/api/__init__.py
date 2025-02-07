from flask import Blueprint

from app.models import User



bp = Blueprint('api', __name__)


from app.api import auth
from app.api import users
from app.api import task


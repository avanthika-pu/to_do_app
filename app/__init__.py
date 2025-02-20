from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS
from sqlalchemy import text
import sqlite3
import redis

db = SQLAlchemy()
migrate = Migrate()

redis_obj = redis.StrictRedis.from_url(Config.REDIS_URL, decode_responses=True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.cli.command("check-db")
    def check_db():
        try:
            db.session.execute(text('SELECT 1')) 
            print("Database connection is successful!")
        except Exception as e:
            print(f"Database connection failed: {str(e)}")

    # Register blueprints
    from app.api.users import user_blueprint
    from app.api.task import task_blueprint
    from app.api.auth import  auth_blueprint

    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(task_blueprint, url_prefix='/task')
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    return app

from app import models

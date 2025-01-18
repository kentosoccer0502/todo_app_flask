from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Initialize the database (ChatGPTを用いて生成)
db = SQLAlchemy()


# Initialize the Flask app (ChatGPTを用いて生成)
def create_app():
    # Create the Flask app
    app = Flask(__name__)
    # Set the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Initialize the database
    db.init_app(app)
    
    # Import the models
    from app.models.todo import Todo
    from app.models.user import User

    # Initialize the migration
    Migrate(app, db)

    # Register the blueprints
    from app.routes.todo import todo_bp
    app.register_blueprint(todo_bp)
    from app.routes.user import user_bp
    app.register_blueprint(user_bp)
    
    return app
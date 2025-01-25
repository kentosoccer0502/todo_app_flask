from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# Initialize the database (ChatGPTを用いて生成)
db = SQLAlchemy()


# Initialize the Flask app (ChatGPTを用いて生成)
def create_app():
    # Create the Flask app
    app = Flask(__name__)
    app.secret_key = 'secret_key'
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

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register the blueprints
    from app.routes.todo import todo_bp
    app.register_blueprint(todo_bp)
    from app.routes.user import user_bp
    app.register_blueprint(user_bp)
    from app.routes.login import login_bp
    app.register_blueprint(login_bp)
    
    return app
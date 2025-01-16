from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Todo, User
from auth import basic_authenticate

# Initialize the Flask app (ChatGPTを用いて生成)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

# Initialize the database (ChatGPTを用いて生成)
db.init_app(app)

# Create a new todo table (ChatGPTを用いて生成)
with app.app_context():
    db.create_all()


## Todo REST API ##
# Add a new todo (ChatGPTを用いて叩き台を生成)
@app.route('/todos', methods=['POST'])
@basic_authenticate
def create_todo(user):
    data = request.get_json()
    try:
        todo_title = data.get('title')
        todo_status = data.get('status', '未着手')
        todo_priority = data.get('priority', 1)
        todo_new = Todo(
            todo_title=todo_title,
            todo_status=todo_status,
            todo_priority=todo_priority,
            user_id=user.id
        )
        db.session.add(todo_new)
        db.session.commit()
        result = {
            'id': todo_new.id,
            'user_id': todo_new.user_id,
            'title': todo_new.todo_title,
            'status': todo_new.todo_status,
            'priority': todo_new.todo_priority,
            'created_at': todo_new.created_at,
            'updated_at': todo_new.updated_at
        }
        return jsonify(f'Added successfully\n {result}'), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 503


# Get all todos
@app.route('/todos', methods=['GET'])
@basic_authenticate
def get_todos(user):
    try:
        todos = Todo.query.filter_by(user_id=user.id).all()
        todos_list = []
        for todo in todos:
            todo_data = {
                'id': todo.id,
                'user_id': todo.user_id,
                'title': todo.todo_title,
                'status': todo.todo_status,
                'priority': todo.todo_priority,
                'created_at': todo.created_at,
                'updated_at': todo.updated_at
            }
            todos_list.append(todo_data)
        return jsonify(todos_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 503


# Update todo
@app.route('/todos/<int:id>', methods=['PUT'])
@basic_authenticate
def update_todo(id, user):
    data = request.get_json()
    try:
        todo_update = Todo.query.filter_by(user_id=user.id).get(id)
        if not todo_update:
            return (f'Error: id:{id} does not exists'), 404
        if 'title' in data:
            todo_update.todo_title = data.get('title')
        if 'status' in data:
            todo_update.todo_status = data.get('status')
        if 'priority' in data:
            todo_update.todo_priority = data.get('priority')
        db.session.commit()
        result = {
            'id': todo_update.id,
            'user_id': todo_update.user_id,
            'title': todo_update.todo_title,
            'status': todo_update.todo_status,
            'priority': todo_update.todo_priority,
            'created_at': todo_update.created_at,
            'updated_at': todo_update.updated_at
        }
        return jsonify(result), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 503
    

# Delete todo
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id, user):
    try:
        todo_delete = Todo.query.filter_by(user_id=user.id).get(id)
        if not todo_delete:
            return (f'Error: id{id} does not exists'), 404
        db.session.delete(todo_delete)
        db.session.commit()
        return jsonify(f'Deleted successfully'), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 503


## User REST API ##
# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'username': user.username,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            users_list.append(user_data)
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 503
    
# Add a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        username = data.get('username')
        password = data.get('password')
        user_new = User(username=username)
        user_new.set_password(password)
        db.session.add(user_new)
        db.session.commit()
        result = {
            'id': user_new.id,
            'username': user_new.username,
            'created_at': user_new.created_at,
            'updated_at': user_new.updated_at
        }
        return jsonify(f'Added successfully\n {result}'), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 503

        
# Run the app (ChatGPTを用いて生成)
if __name__ == '__main__':
    app.run(debug=True)
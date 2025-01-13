from flask import Flask, request, jsonify
from models import db, Todo


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create a new todo table
with app.app_context():
    db.create_all()


# Add a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    try:
        todo_title = data.get('title')
        todo_new = Todo(todo_title=todo_title)
        db.session.add(todo_new)
        db.session.commit()
        result = {
            'id': todo_new.id,
            'title': todo_new.todo_title,
            'created_at': todo_new.created_at,
            'updated_at': todo_new.updated_at
        }
        return jsonify(result), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 503


# Get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    try:
        todos = Todo.query.all()
        todos_list = []
        for todo in todos:
            todo_data = {
                'id': todo.id,
                'title': todo.todo_title,
                'created_at': todo.created_at,
                'updated_at': todo.updated_at
            }
            todos_list.append(todo_data)
        return jsonify(todos_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 503


# Update todo
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    try:
        todo_update = Todo.query.get(id)
        if not todo_update:
            return (f'Error: id{id} does not exists'), 404
        todo_update.todo_title = data.get('title')
        db.session.commit()
        result = {
            'id': todo_update.id,
            'title': todo_update.todo_title,
            'created_at': todo_update.created_at,
            'updated_at': todo_update.updated_at
        }
        return jsonify(result), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 503
    

# Delete todo
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        todo_delete = Todo.query.get(id)
        if not todo_delete:
            return (f'Error: id{id} does not exists'), 404
        db.session.delete(todo_delete)
        db.session.commit()
        return jsonify(f'Deleted successfully'), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 503

        

if __name__ == '__main__':
    app.run(debug=True)
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from app import db
from app.models.todo import Todo
from app.utils.auth import basic_authenticate

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/todos/add', methods=['POST'])
@login_required
def create_todo():
    data = request.form
    try:
        todo_title = data.get('title')
        todo_status = data.get('status', '未着手')
        todo_priority = data.get('priority', 1)
        todo_new = Todo(
            todo_title=todo_title,
            todo_status=todo_status,
            todo_priority=todo_priority,
            user_id=current_user.id,
        )
        db.session.add(todo_new)
        db.session.commit()
        return redirect(url_for('todo.get_todos'))
    except Exception as e:
        return jsonify({'error': str(e)}), 503


@todo_bp.route('/todos', methods=['GET'])
@login_required
def get_todos():
    try:
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        todos_list = []
        for todo in todos:
            todo_data = {
                'id': todo.id,
                'user_id': todo.user_id,
                'todo_title': todo.todo_title,
                'todo_status': todo.todo_status,
                'todo_priority': todo.todo_priority,
                'created_at': todo.created_at,
                'updated_at': todo.updated_at
            }
            todos_list.append(todo_data)
        return render_template(
            'index.html', user=current_user, todos=todos_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 503


@todo_bp.route('/todos/update/<int:id>', methods=['PUT'])
@basic_authenticate
def update_todo(user, id):
    data = request.get_json()
    try:
        todo_update = Todo.query.filter(
            Todo.id == id, Todo.user_id == user.id).first()
        if not todo_update:
            return (f'Error: id:{id} does not exists'), 404
        if 'title' in data:
            todo_update.todo_title = data.get('title')
        if 'status' in data:
            todo_update.todo_status = data.get('status')
        if 'priority' in data:
            todo_update.todo_priority = data.get('priority')
        db.session.commit()
        return redirect(url_for('todo.index')), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 503


@todo_bp.route('/todos/delete/<int:todo_id>', methods=['DELETE'])
@basic_authenticate
def delete_todo(todo_id):
    try:
        todo_delete = Todo.query.filter(
            Todo.id == todo_id,
            Todo.user_id == current_user.id).first()
        if not todo_delete:
            return (f'Error: id{todo_id} does not exists'), 404
        db.session.delete(todo_delete)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 503

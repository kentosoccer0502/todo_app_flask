from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from app import db
from app.models.todo import Todo
from app.utils.auth import basic_authenticate

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/todos', methods=['GET'])
@login_required
def get_todos():
    try:
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        todos_list = []
        for todo in todos:
            data = {
                'id': todo.id,
                'user_id': todo.user_id,
                'title': todo.title,
                'status': todo.status,
                'priority': todo.priority,
                'created_at': todo.created_at,
                'updated_at': todo.updated_at
            }
            todos_list.append(data)
        return render_template(
            'main.html', user=current_user, todos=todos_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 503


@todo_bp.route('/todos', methods=['POST'])
@login_required
def create_todo():
    data = request.form
    try:
        title = data.get('title')
        status = data.get('status', '未着手')
        priority = data.get('priority', 1)
        todo_new = Todo(
            title=title,
            status=status,
            priority=priority,
            user_id=current_user.id,
        )
        db.session.add(todo_new)
        db.session.commit()
        return redirect(url_for('todo.get_todos')), 302
    except Exception as e:
        return jsonify({'error': str(e)}), 503


@todo_bp.route('/todos/<int:id>', methods=['POST'])
@login_required
def modify_todo(id):
    method = request.form.get('_method', '')
    if method == 'PUT':
        return update_todo(id)
    elif method == 'DELETE':
        return delete_todo(id)
    else:
        return jsonify({'error': 'Invalid method'}), 400


def update_todo(id):
    data = request.form
    try:
        todo_update = Todo.query.filter(
            Todo.id == id,
            Todo.user_id == current_user.id).first()
        if not todo_update:
            return (f'Error: id:{id} does not exists'), 404
        if 'title' in data:
            todo_update.title = data.get('title')
        if 'status' in data:
            todo_update.status = data.get('status')
        if 'priority' in data:
            todo_update.priority = data.get('priority')
        db.session.commit()
        return redirect(url_for('todo.get_todos')), 302
    except Exception as e:
        return jsonify({'error': str(e)}), 503


def delete_todo(id):
    try:
        todo_delete = Todo.query.filter(
            Todo.id == id,
            Todo.user_id == current_user.id).first()
        if not todo_delete:
            return (f'Error: id{id} does not exists'), 404
        db.session.delete(todo_delete)
        db.session.commit()
        return redirect(url_for('todo.get_todos')), 302
    except Exception as e:
        return jsonify({'error': str(e)}), 503

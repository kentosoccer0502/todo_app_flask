from flask import Blueprint, request, jsonify

from app import db
from app.models.user import User

user_bp = Blueprint('user', __name__)

## User REST API ###############################################################################################################
# Get all users(/todos/addのPOSTメソッドを参考にして自力で作成)
@user_bp.route('/users', methods=['GET'])
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
    

# Add a new user(/todos/addのPOSTメソッドを参考にして自力で作成)
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        username = data.get('username')
        password = data.get('password')
        user_new = User(username=username)
        user_new.set_password(password)
        db.session.add(user_new)
        db.session.commit()
        return jsonify(f'Added successfully! {user_new.username}'), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 503
from flask import request, jsonify
from functools import wraps
from werkzeug.security import check_password_hash

from models import User

# Basic authentication decorator(ChatGPTを用いて生成)
# 入力プロンプト:
# user_idをTodoテーブルに追加したことによって、/todoのREST APIにて、コードはどのように改修すべきでしょうか？
# おそらくパスワード入力が必要になる認識です。
def basic_authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({'message': 'Could not verify your access'}), 401
        
        user = User.query.filter_by(username=auth.username).first()
        if not user or not check_password_hash(user.password_hash, auth.password):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        return func(user, *args, **kwargs)
    
    return wrapper
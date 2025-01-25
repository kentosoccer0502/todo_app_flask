from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from app.models.user import User
from app.routes import todo

login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ユーザーの存在確認
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('Login Successed!', 'success')
            return redirect(url_for('todo.get_todos'))  # Top Pageにリダイレクト
        else:
            flash('Username or password is wrong', 'danger')
            return redirect(url_for('login.login'))
    return render_template('login.html')


@login_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login.login'))

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash

from app.models.user import User


login_bp = Blueprint('login', __name__) 


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ユーザーの存在確認
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['username'] = username  # セッションにユーザーIDを保存
            flash('Login Successed!', 'success')
            return redirect(url_for('login.dashboard'))  # ダッシュボードにリダイレクト
        else:
            flash('Username or password is wrong', 'danger')
            return redirect(url_for('login.login'))
    return render_template('login.html')

@login_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Login required', 'warning')
        return redirect(url_for('login'))
    return f"Welcome User {session['username']} "

@login_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logout Successed!', 'success')
    return redirect(url_for('login'))
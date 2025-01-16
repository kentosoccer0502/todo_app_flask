from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the database (ChatGPTを用いて生成)
db = SQLAlchemy()

# Create a new todo table (叩き台をChatGPTを用いて生成)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_title = db.Column(db.String(200), nullable=False)
    todo_status = db.Column(db.String(10), nullable=True)
    todo_priority = db.Column(db.Integer, nullable=False, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# Create a new user table (叩き台をChatGPTを用いて生成)
# 入力プロンプト
# user テーブルを以下の要件で作成したい。
#・id, username, passwordのカラムを設ける
#・idを主キーとする
#・passwordはハッシュ化してDBに保存する
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
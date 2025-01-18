from datetime import datetime

from app import db


# Create a new todo table (叩き台をChatGPTを用いて生成)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_title = db.Column(db.String(200), nullable=False)
    todo_status = db.Column(db.String(10), nullable=True)
    todo_priority = db.Column(db.Integer, nullable=False, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the database (ChatGPTを用いて生成)
db = SQLAlchemy()

# Create a new todo table (叩き台をChatGPTを用いて生成)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
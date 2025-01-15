# ca_techlounge_kadai

## 本レポジトリについて
本レポジトリは、CA Tech Lounge提出型選考の課題の提出物である。
TODOリストを管理するREST APIを課題の必須要件および任意の追加要件をもとに開発した。


## 考察


### 気づいた点

### 工夫点

### 技術の選定理由


## 動作確認方法

## 開発する上で参照した情報
1\. ChatGPT

叩き台を以下のプロンプトを入力して引用した。

* プロンプト
```
Flaskを用いて、TODOリストを管理するREST APIを作成したい。
以下を参照して提示してください。

# ルール
STEPごとに作成する

# Step1
タイトルを指定してTODOを作成するAPI

# 要件
- SQLAlchemyを利用すること
- タイトルをDBに保存すること（一意のID、タイトル、created_at、updated_at）
- ステータスコード
```
* 引用したコード（生成されたコード）
```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# モデル定義
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# DB初期化
with app.app_context():
    db.create_all()

# TODO作成API
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    new_todo = Todo(title=title)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({
        'id': new_todo.id,
        'title': new_todo.title,
        'created_at': new_todo.created_at,
        'updated_at': new_todo.updated_at
    }), 201

if __name__ == '__main__':
    app.run(debug=True)
```




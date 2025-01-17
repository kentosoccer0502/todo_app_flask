# ca_techlounge_kadai

## 本レポジトリについて
### 概要
本レポジトリは、CA Tech Lounge提出型選考の課題の提出物である。
TODOリストを管理するREST APIを課題の必須要件および任意の追加要件をもとに開発した。
### 技術構成
* プログラミング言語：Python
* Framework：Flask
* データベース：SQLite(SQLAlchemyツール利用)

## 考察
### 気づいた点

### 工夫点

### 技術の選定理由
* 学習コスト
   * 業務でPythonやFlaskを利用していたことから、本技術を活用した。
* シンプルさ
   * PythonやFlaskは可読性が高いかつシンプルな構成の上、本課題の要件を満たすための十分な機能を有していたため
* 挑戦
   * ウェブアプリ開発ではMongoDBなどのNoSQLを利用したことがあったが、RDBでの開発に挑戦したかったため、SQLiteを採用した

## 動作確認方法
* 動作環境(確認済み)
  * python: 3.8.5
  * pip: 24.3.1
  * OS: MacOS

1\. ローカルマシンにコードをClone
```bash
git clone https://github.com/catechlounge/kento_natsuyama.git
```

2\. 環境構築
```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 必要なパッケージのインストール
pip install -r requirements.txt

```

3\. アプリケーションの起動
```bash
python app.py
```

4\. 別セッションでユーザの新規作成(userおよびpasswordは例)
```bash
curl -i -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{
  "username": "testuser",
  "password": "securepassword123"
}'
```

5\. ユーザ一覧を取得
```bash
curl -i -X GET http://127.0.0.1:5000/users
```

6\. タイトルを指定してTODOを作成するAPI(userおよびpasswordは例)
```bash
curl -i -X POST -u testuser:securepassword123 http://127.0.0.1:5000/todos \
-H "Content-Type: application/json" \
-d '{
  "title": "Learn Flask",
  "status": "未着手",
  "priority": 1
}'
```

7\. 作成したTODOの一覧を取得するAPI(userおよびpasswordは例)
```bash
curl -i -X GET -u testuser1:securepassword123 http://127.0.0.1:5000/todos
```

8\. 指定したTODOを変更するAPI(userおよびpasswordは例)
```bash
curl -i -X PUT -u testuser1:securepassword123 http://127.0.0.1:5000/todos/1 \
-H "Content-Type: application/json" \
-d '{
  "title": "Learn Flask Basics",
  "status": "進行中",
  "priority": 2
}'

```

9\. 指定したTODOを削除するAPI(userおよびpasswordは例)
```bash
curl -i -X DELETE -u testuser1:securepassword123 http://127.0.0.1:5000/todos/1
```


## 開発する上で引用した情報
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




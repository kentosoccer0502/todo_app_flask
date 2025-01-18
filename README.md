# ca_techlounge_kadai

## 本レポジトリについて
### 概要
本レポジトリは、CA Tech Lounge提出型選考の課題の提出物である。
TODOリストを管理するREST APIを課題の必須要件および任意の追加要件をもとに開発した。
### 技術構成
* プログラミング言語：Python
* Framework：Flask
* データベース：SQLite(SQLAlchemyツール利用)
* コンテナ：Docker

## 考察
### 気づいた点
* RDBを用いたウェブアプリケーション開発の難しさ
   * 今までは主にNoSQLのMongoDBを使った開発を行っていたので、それと比較して以下の点が難しく感じた
      * カラムの追加などのDBのスキーマの変更の都度、適用が必要な点
      * 主キーや外部キーを意識する必要がある点
      * スキーマの変更の適用がうまくいかない場合が多々あった点
* 適切なエラーハンドリングの設計の重要さ
   * エラーハンドリングを適切に実装することで、クライアント側でのデバッグが容易になるため、改めて重要性を感じた
   * ただ、さらに詳細にエラーハンドリングできる余地は十分にあるので、改善ができると感じる
* コンテナでアプリケーションを起動するためには、127.0.0.1ではなく、0.0.0.0でLISTENしておく必要があることを学んだ
   * 最初はデフォルト設定の127.0.0.1で、コンテナ内で起動していたが、クライアント側からアクセス拒否される事象のトラブルシューティング時に気づいた

### 工夫点
* 可読性
   * modelsやauthをモジュール化することにより、コードを分割してコードの冗長化を防止した
   * 変数名や関数名は規則性および何を表しているかをわかることを意識した
* 使える機能を実装すること
   * 他のユーザが実際に使ってもらえるような機能を設けること（ユーザごとにTODOの管理可能、優先度／ステータスカラム、エラーハンドリングなど）
* ユーザごとにTODOを管理可能
   * user_idを利用しユーザごとに独立したTODO管理を可能とした
   * 認証機能を実装することによって、セキュアにユーザがTODO管理をできるようにした
* エラーハンドリングの工夫
   * 例外処理try-exceptを利用し、データベース操作や認証エラーなどを適切に処理できるように意識した
   * 503や401エラーなど、状況に応じたレスポンスを実装

### 技術の選定理由
* 学習コスト
   * 業務でPythonやFlaskを利用していたことから、本技術を活用した。
* シンプルさ
   * PythonやFlaskは可読性が高いかつシンプルな構成の上、本課題の要件を満たすための十分な機能を有していたため
* 挑戦
   * ウェブアプリケーション開発ではMongoDBなどのNoSQLを利用したことがあったが、RDBでの開発に挑戦したかったため、SQLiteを採用した
   * Dockerは資格試験の学習時や業務の維持管理業務で触ったことがあったが、今回のように自分で開発したアプリケーションをコンテナ上で起動させることはしたことがなく、試してみたかったため

## 動作確認方法
* 動作環境(確認済み)
  * python: 3.8.5
  * pip: 24.3.1
  * OS: MacOS

1\. ローカルマシンにコードをClone
```bash
git clone https://github.com/catechlounge/kento_natsuyama.git
```

2\. コンテナビルド／起動
```bash
#　ビルド（イメージ名は例）
docker build -t flask-todo-app .

# コンテナ起動（コンテナ名は任意）
docker run -d -p 5000:5000 --name flask-todo-container flask-todo-app

```

3\. 別セッションでユーザの新規作成(userおよびpasswordは例)
```bash
curl -i -X POST http://127.0.0.1:5000/users \
-H "Content-Type: application/json" \
-d '{
  "username": "testuser",
  "password": "securepassword123"
}'
```

4\. ユーザ一覧を取得
```bash
curl -i -X GET http://127.0.0.1:5000/users
```

5\. タイトルを指定してTODOを作成するAPI(userおよびpasswordは例)
```bash
curl -i -X POST -u testuser1:securepassword123 http://127.0.0.1:5000/todos \
-H "Content-Type: application/json" \
-d '{
  "title": "Learn Flask",
  "status": "未着手",
  "priority": 1
}'
```

6\. 作成したTODOの一覧を取得するAPI(userおよびpasswordは例)
```bash
curl -i -X GET -u testuser1:securepassword123 http://127.0.0.1:5000/todos
```

7\. 指定したTODOを変更するAPI(userおよびpasswordは例)
```bash
curl -i -X PUT -u testuser1:securepassword123 http://127.0.0.1:5000/todos/1 \
-H "Content-Type: application/json" \
-d '{
  "title": "Learn Flask Basics",
  "status": "進行中",
  "priority": 2
}'

```

8\. 指定したTODOを削除するAPI(userおよびpasswordは例)
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




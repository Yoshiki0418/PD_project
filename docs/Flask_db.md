# FlaskとMySQLの接続
## 1. 必要なパッケージのインストール
まず、FlaskとFlask-SQLAlchemy、そしてMySQLを扱うためのドライバをインストールします。

```bash
pip3 install flask flask_sqlalchemy pymysql
```
ここでpymysqlは、PythonでMySQLデータベースを操作するためのライブラリです。

## 2. Flaskアプリケーションの設定
次に、Flaskアプリケーションを設定し、SQLAlchemyでMySQLデータベースに接続します。

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQLデータベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```
ここで、username、password、localhost、dbnameは、それぞれMySQLデータベースのユーザー名、パスワード、ホスト名、データベース名に置き換えてください。

## 3. モデルの定義
次に、データベースのテーブルに対応するモデルを定義します。

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
```

## 4. データの操作
Flaskアプリケーション内でデータベースにデータを追加したり、データを取得したりすることができます。

```python
# データの追加
new_user = User(username='user1', email='user1@example.com')
db.session.add(new_user)
db.session.commit()

# データの取得
users = User.query.all()
print(users)
```
### ※注意事項
セキュリティ: データベースの認証情報をソースコードに直接記述することは避け、環境変数や設定ファイルを使用することが推奨されます。
エラーハンドリング: データベース操作中にエラーが発生した場合、適切にエラーを処理することが重要です。

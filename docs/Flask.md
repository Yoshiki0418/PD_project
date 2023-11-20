# Flaskのセットアップ
## １. Flaskのインストール
仮想環境内でFlaskをインストールします。

```bash
pip3 install Flask
```

## 2. 最初のFlaskアプリケーション
#### a. アプリケーションの作成
Flaskアプリケーションの基本的な構造を作成します。以下のようにapp.pyというファイルを作成し、基本的なFlaskアプリケーションのコードを記述します。

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```
#### b. アプリケーションの実行
以下のコマンドでFlaskアプリケーションを実行します。

```bash
python app.py
```
#### c. アプリケーションへのアクセス
ブラウザを開き、http://127.0.0.1:5000/ にアクセスします。 "Hello, World!"と表示されれば成功です。

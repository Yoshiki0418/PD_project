# PD_project
## 冷蔵庫管理システム
- 完成予定:1月
- オンプレミス版(クラウド版はこのプロジェクトが終了次第挑戦予定)
- URL:
  
## 目的
食品ロスを減らすために、画像処理を用いて食材管理を手軽にできるサービスを目指しています。

## 特徴

- 食材の画像を撮影するだけで、作成できるレシピを考案する
- 冷蔵庫の中身を撮影するだけで、食材情報を管理
- 機械学習を通して、食材の消費を予測した買い物の提案（クラウド版で実装予定）

## 開発メモ（実現したいこと）
- レシピ情報ページで、データベース情報から足りない食材を参照し、足りない食材を違う色で表示し、買い物リストに追加できる機能の搭載
- レシピテーブルに材料の量を示す単位や個数を追加し、人数に応じた材料量を表示させる。

  ↪︎そのレシピが作成されたら、その量だけ材料を減らせるようにテーブルの情報を更新
- ユーザーの食材消費量を学習させて、無駄な買い物を減らす

## 技術スタック

- HTML/CSS
- JavaScript
- Python(Flask)
  
## 仕様ツール
- Vision API
- Open AI API
- teachable machine
- OpenCV

## MySQLセットアップ
### 1. MySQLサーバーのインストール
MySQLがまだインストールされていない場合は、公式のMySQLダウンロードページ https://dev.mysql.com/downloads/mysql/ からインストーラーをダウンロードしてインストールしてください。
#### ターミナルでインストール
- macOS
  
1. Homebrewを使用:
macOSでは、パッケージマネージャーのHomebrewを使用してMySQLをインストールすることが一般的です。まず、ターミナルを開きます。

```bash
brew update
brew install mysql
```

2. MySQLの自動起動設定（オプション）:
MySQLをシステム起動時に自動的に起動させたい場合は、以下のコマンドを実行します。

```bash
brew services start mysql
```

3. MySQLのセキュリティ設定:
初期セキュリティ設定を行います。

```bash
mysql_secure_installation
```

4. MySQLへのログイン:
MySQLコマンドラインツールにログインします。

```bash
Copy code
mysql -u root -p
```
.
- Windows(インストーラーからする方が楽)
1. MySQLインストーラーのダウンロード:
Windowsでは、MySQLの公式サイトからMySQLインストーラーをダウンロードし、実行します。

2. インストール手順に従う:
インストーラーの指示に従ってMySQLをインストールします。インストーラーでは、MySQLサーバーの他にもMySQL Workbenchなどのツールをインストールするオプションがあります。

3. 初期セットアップ:
インストールプロセスの一部として、MySQLサーバーの初期セットアップ（rootユーザーのパスワード設定など）が行われます。

4. MySQL Workbenchの使用:
MySQL Workbenchを使用してMySQLサーバーに接続し、データベースの作成やユーザーの管理を行うことができます。**


## 2. データベースの作成
MySQLコマンドラインツールを使用して、新しいデータベースを作成します。以下のコマンドを実行してください：
```sql
CREATE DATABASE your_database_name;
```
your_database_name をプロジェクト用のデータベース名に置き換えてください。

## 3. データベースユーザーの作成と権限の付与
セキュリティを強化するために、プロジェクト専用のユーザーを作成し、作成したデータベースに対する権限を付与します。以下のコマンドを実行してください：
```sql
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;
```
your_username と your_password を適切な値に置き換えてください。

## セットアップ

```bash
Coming Soon



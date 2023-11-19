# MySQLセットアップ
## 1. MySQLサーバーのインストール
MySQLがまだインストールされていない場合は、公式の[MySQLダウンロードページ](https://dev.mysql.com/downloads/mysql/)からインストーラーをダウンロードしてインストールしてください。
### ターミナルでインストール
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

## 4.テーブルの作成
- [食材テーブル](resource/vegetable.csv)
  
| Field           | Type         | Null | Key | Default | Extra          |
------------------|--------------|------|-----|---------|----------------|
| IngredientID    | int          | NO   | PRI | NULL    | auto_increment |
| name            | varchar(255) | NO   |     | NULL    |                |
| expiration_date | date         | YES  |     | NULL    |                |
| image_path      | varchar(255) | YES  |     | NULL    |                |
| is_present      | tinyint(1)   | YES  |     | 1       |                |
| Category        | int          | YES  |     | NULL    |                |

＃以下のコマンドでテーブルを作成
```sql
CREATE TABLE Ingredients (
    IngredientID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    expiration_date DATE,
    image_path VARCHAR(255),
    is_present TINYINT(1) DEFAULT 1,
    Category INT
);
```
次に、以下のコマンドを実行します：

```sql
LOAD DATA INFILE '/path/to/vegetable.csv' 
INTO TABLE Ingredients 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 LINES;
```
※/path/to/vegetable.csvはCSVファイルのパスを指定します。実際のファイルパスに置き換えてください。

- レシピテーブル
 
| Field        | Type         | Null | Key | Default | Extra |
|--------------|--------------|------|-----|---------|-------|
| RecipeID     | int          | NO   | PRI | NULL    |       |
| RecipeName   | varchar(255) | NO   |     | NULL    |       |
| Description  | text         | YES  |     | NULL    |       |
| CookingTime  | int          | YES  |     | NULL    |       |
| ImageURL     | varchar(255) | YES  |     | NULL    |       |
| Ingredients  | text         | YES  |     | NULL    |       |
| Instructions | text         | YES  |     | NULL    |       |

- カテゴリーテーブル

| Field        | Type         | Null | Key | Default | Extra |
|--------------|--------------|------|-----|---------|-------|
| CategoryID   | int          | NO   | PRI | NULL    |       |
| CategoryName | varchar(255) | NO   |     | NULL    |       |


- 食材とレシピの中間テーブル

| Field        | Type | Null | Key | Default | Extra          |
|--------------|------|------|-----|---------|----------------|
| ID           | int  | NO   | PRI | NULL    | auto_increment |
| IngredientID | int  | YES  | MUL | NULL    |                |
| RecipeID     | int  | YES  | MUL | NULL    |                |

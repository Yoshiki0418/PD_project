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

## セットアップ
### MySQL
1. MySQLサーバーのインストール
MySQLがまだインストールされていない場合は、公式のMySQLダウンロードページ https://dev.mysql.com/downloads/mysql/ からインストーラーをダウンロードしてインストールしてください。

2. データベースの作成
MySQLコマンドラインツールを使用して、新しいデータベースを作成します。以下のコマンドを実行してください：
```sql
CREATE DATABASE your_database_name;
```
your_database_name をプロジェクト用のデータベース名に置き換えてください。

3. データベースユーザーの作成と権限の付与
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



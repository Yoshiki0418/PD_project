# PD_project - 冷蔵庫管理システム

食品ロスを減らすために、画像処理を用いて食材管理を手軽にできるサービスです。

## デモ動画

[![Watch the video](https://img.youtube.com/vi/wmUcvecm1J0/maxresdefault.jpg)](https://www.youtube.com/watch?v=wmUcvecm1J0)

## 執筆記事

https://zenn.dev/yoshi_tech/articles/ad3aaa1cd55c73

## 特徴

- 📸 食材の画像を撮影するだけで、作成できるレシピを提案
- 🧊 冷蔵庫の中身を撮影するだけで、食材情報を自動管理
- 🤖 機械学習（YOLO / Keras）による食材認識
- 🍽️ 味の素パークからのレシピスクレイピング
- 📊 栄養素の自動計算

## アーキテクチャ

![image](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3687042/6ec179bf-e116-5957-eb9f-fc9e7fc7df5b.png)

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| バックエンド | Python (Flask) |
| フロントエンド | HTML / CSS / JavaScript |
| データベース | MySQL / SQLite |
| 画像認識 | TensorFlow / Keras / YOLO (ultralytics) |
| OCR | Google Cloud Vision API |
| 認証 | Firebase Authentication |

## プロジェクト構成

```
PD_project/
├── app/                    # Flask アプリケーションパッケージ
│   ├── __init__.py         # Application Factory
│   ├── config.py           # 設定
│   ├── models.py           # データベースモデル
│   ├── routes/             # ルート定義 (Blueprint)
│   │   ├── main.py         # メインページ
│   │   ├── foods.py        # 食材管理
│   │   └── recipes.py      # レシピ管理
│   └── services/           # ビジネスロジック
│       ├── food_judge.py   # 食材画像判定
│       ├── meat_judge.py   # 肉分類 (Vision API)
│       ├── object_detection.py  # YOLO 物体検出
│       ├── scraping.py     # レシピスクレイピング
│       ├── nutrition.py    # 栄養計算
│       └── unit_conversion.py   # 単位変換
├── static/                 # 静的ファイル (CSS/JS/画像)
├── templates/              # HTML テンプレート
├── model/                  # ML モデルファイル
├── migrations/             # DB マイグレーション
├── docs/                   # ドキュメント
├── .devcontainer/          # Dev Container 設定
├── run.py                  # アプリ起動スクリプト
└── requirements.txt        # Python 依存関係
```

## セットアップ

### 1. リポジトリのクローン

```bash
git clone --recurse-submodules https://github.com/Yoshiki0418/PD_project.git
cd PD_project
```

### 2. ML モデルファイルの配置

以下のファイルを `model/` ディレクトリに配置してください:

- `new_keras_model.h5` - 食材分類モデル
- `new_labels.txt` - ラベルファイル

### 3. 環境変数の設定

```bash
cp .env.example .env
# .env ファイルを編集して必要な値を設定
```

### 4. Docker を使用する場合（推奨）

```bash
# Dev Container で起動
# VS Code の「Reopen in Container」を使用
```

### 5. ローカルで起動する場合

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

サーバーが `http://localhost:5000` で起動します。

## 開発ドキュメント

詳細な技術ドキュメントは [docs/](docs/) を参照してください。

- [Flask セットアップ](docs/Flask.md)
- [MySQL セットアップ](docs/MySQL.md)
- [画像処理精度について](docs/Image_processing_evaluation.md)
- [物体検出の評価指標](docs/camera.md)

## ライセンス

This project is for educational purposes.

# PD_project
## 冷蔵庫管理システム
- 制作期間:4ヶ月
- オンプレミス版
  
## 目的
食品ロスを減らすために、画像処理を用いて食材管理を手軽にできるサービスを目指しています。

## アプリの説明動画

[![Watch the video](https://img.youtube.com/vi/wmUcvecm1J0/maxresdefault.jpg)](https://www.youtube.com/watch?v=wmUcvecm1J0)
https://www.youtube.com/watch?v=wmUcvecm1J0

## 執筆
https://zenn.dev/yoshi_tech/articles/ad3aaa1cd55c73

## アーキテクチャ

![image](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3687042/6ec179bf-e116-5957-eb9f-fc9e7fc7df5b.png)

## 特徴

- 食材の画像を撮影するだけで、作成できるレシピを考案する
- 冷蔵庫の中身を撮影するだけで、食材情報を管理
- 機械学習を通して、食材の消費を予測した買い物の提案（クラウド版で実装予定）

## 開発メモ（実現したいこと）
- レシピ情報ページで、データベース情報から足りない食材を参照し、足りない食材を違う色で表示し、買い物リストに追加できる機能の搭載
- レシピテーブルに材料の量を示す単位や個数を追加し、人数に応じた材料量を表示させる。

  ↪︎そのレシピが作成されたら、その量だけ材料を減らせるようにテーブルの情報を更新
- ユーザーの食材消費量を学習させて、無駄な買い物を減らす

## 開発ToDoリスト
### [TODO📖](https://github.com/users/Yoshiki0418/projects/3/views/1)

## システム構築メモ
### 複数の食材検知をどう実現するか
-  [AutoML Vision(GCP)](https://cloud.google.com/vision/automl/docs/label-images?hl=ja)
-  Amazon Rekognition(AWS)
-  [YoLo](https://farml1.com/yolov8/)

## 評価指標
### 　技術指標
- [画像処理精度について](Image_processing_evaluation.md)
- [物体検出の評価指標](camera.md)

## 技術スタック

- HTML/CSS
- JavaScript
- Python(Flask)
  
## 使用ツール
- Vision API
- Open AI API
- teachable machine
- OpenCV

## セットアップ
### サーバーサイド
- [Flaskのセットアップ](Flask.md)
### データベース
- [MySQLのセットアップ](MySQL.md)
- [Flaskでデータベースを定義する](Flask_db.md)

## 学習
- [なぜ、前処理方法を変更して画像処理の精度が上がったのか](Improved_accuracy.md)
- [アノテーションとは](annotation.md)
- [理想的な物体検出データセットの構築](datasets.md)

  











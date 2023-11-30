# アノテーションとは
データ（特に画像やテキストなど）に追加情報を付与するプロセスのことを指します。この追加情報は、特定の目的（例えば、機械学習モデルのトレーニング）に役立てるために使用されます。アノテーションは、特にコンピュータビジョンや自然言語処理の分野で重要です。

# アノテーションの種類
- [画像・映像データ](##画像・映像データ)
- [音声データ](##音声データ)
- [テキストデータ](##テキストデータ)

## 画像・映像データ
### 1.バウンディングボックス
画像内の特定のオブジェクトを囲む矩形を描き、そのオブジェクトを識別します。
バウンディングボックスの主な表現方法は、コーナー2点による表現と、中心点と幅・高さを使う表現の2種類があります。

&nbsp;
### 2.セグメンテーション
定義: 画像を複数のオブジェクトに分割する技術。

カテゴリ: 画像分類、物体検出、画像セグメンテーション。

&nbsp;
### [セグメンテーションの種類]
#### ・セマンティックセグメンテーション

ピクセル単位でのラベル付け。
空や道路などの不定形領域の検出に適している。


#### ・インスタンスセグメンテーション

物体ごとの領域分割と種類の認識。
隣接する物体の区別に有効。

#### ・パノプティックセグメンテーション

セマンティックとインスタンスセグメンテーションの組み合わせ。
画像内のすべてのピクセルにタグ付け。

&nbsp;
### セグメンテーション技法
- FCN (Fully Convolutional Network): 画像の物体や顔の認識に有効。

- SegNet: 道路画像の画素単位の分割に利用。

- FPN (Feature Pyramid Networks): 画像認識の検出精度向上。

- R-CNN (Region-Convolutional Neural Network): 物体検出に利用。

- RNN (Recurrent Neural Network): 連続的な情報を持つデータに適用。

&nbsp;
### セグメンテーションの活用事例
- 自動運転: 周囲の物体の瞬時認識。
- 顔認証: 精度の高い識別。
- 外観検査: 製造業での異常検知。
- 医療画像診断: 高精度の診断支援。
- AIドローン: 農業や点検作業での応用。

##### [参考文献](https://aismiley.co.jp/ai_news/semantic_segmentation/)

&nbsp;
### 3.ランドマークアノテーション
顔認識などに使用され、顔の特定のポイント（目、鼻、口など）にマークを付けます。

&nbsp;
### 4.ポリゴンセグメンテーション
多角形での領域指定とは、画像・映像に映った物体の領域を多角形で囲っていくアノテーション手法のことです。多角形で領域を指定していくことにより、正確に領域をアノテーションできます。


## 音声データ

## テキストデータ
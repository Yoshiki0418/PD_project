# 物体検出の評価指標

物体検出は、画像内のオブジェクトの位置とカテゴリを同時に予測するタスクです。この資料では、物体検出モデルの性能を評価するための主要な指標について説明します。

## 精度 (Precision)

精度は、正しく識別されたインスタンスの割合です。式は以下の通りです。

Precision = True Positives / (True Positives + False Positives)

ここで、`True Positives` (TP) はモデルが正しく正と予測したインスタンスの数、`False Positives` (FP) は誤って正と予測したインスタンスの数を指します。

## 再現率 (Recall)

再現率は、実際に正のクラスに属するインスタンスのうち、正しく識別されたものの割合です。

Recall = True Positives / (True Positives + False Negatives)

ここで、`False Negatives` (FN) は実際は正であるにもかかわらず、モデルが誤って負と予測したインスタンスの数を指します。

## F1スコア (F1 Score)

F1スコアは、精度と再現率の調和平均です。

F1 = 2 * (Precision * Recall) / (Precision + Recall)

精度と再現率のどちらも高い値を持つモデルは、F1スコアも高くなります。このスコアは、一方の指標が極端に高い値を示している場合にも、モデルの性能をバランス良く評価するのに有用です。

## 平均精度 (Average Precision, AP)

平均精度は、異なる閾値における精度と再現率の曲線（PR曲線）の下の領域の平均を測ります。APは、モデルが異なる信頼度閾値においてどの程度うまく性能を発揮するかを示す指標であり、0から1までの値を取ります。1に近いほど性能が高いことを意味します。APは、一般に以下のように計算されます：

AP = Σ(R(n) - R(n-1)) P(n)

ここで、`P(n)`は閾値がnのときの精度、`R(n)`は閾値がnのときの再現率です。

mAPは、すべてのクラスにわたるAPの平均値です。物体検出タスクでは、mAPが最も重要な単一指標とされています。

## Intersection Over Union (IOU)

IOUは、予測されたバウンディングボックスと実際のバウンディングボックスの重なりを測定する指標です。

IOU = Area of Overlap / Area of Union

`IOU`は、0から1までの値を取り、1に近いほど予測が正確であることを意味します。

## mAP@IoU Thresholds

異なるIOUの閾値で計算されるmAPを表します。一般的には、IOUの閾値を0.5から0.95まで0.05刻みで変化させた場合のmAPの平均を指します。

## 結論

物体検出モデルの性能評価には複数の指標が重要であり、それぞれが異なる側面を捉えています。最終的なモデル選択には、タスクの目的に最も適した指標を考慮する必要があります。

## 参考文献
- [Evaluation Metrics for Object Detection](https://debuggercafe.com/evaluation-metrics-for-object-detection/)




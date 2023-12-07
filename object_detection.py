import sys
sys.path.append('ultralytics')  # ultralyticsが含まれるディレクトリへのパスを追加

from ultralytics import YOLO
import numpy as np

translation_dict = {
    'tomato': 'トマト',
    'ninnzinn': '人参',
    'jyagaimo': 'じゃがいも',
    'tamanegi': '玉ねぎ',
    'piimann': 'ピーマン',
    'kabocha': 'かぼちゃ',
    'nasu': 'なす',
    'negi': 'ねぎ',
    'daikon': '大根',
    'asuparagasu': 'アスパラガス',
    'rennkonn': 'れんこん',
    'reatsu': 'レタス',
    'satumaimo': 'さつまいも',
    'hourennsou': 'ほうれん草',
    'kyuuri': 'きゅうり',
    'burokkorii': 'ブロッコリー',
    'chinngennsai': '青梗菜',
    'toumorokoshi': 'とうもろこし',
    'niku': '肉',
    'youguruto': 'ヨーグルト',
    'nattou': '納豆',
    'tamago': '卵',
    'kyabetu': 'キャベツ',
    'hakusai': '白菜'
}

def translate_to_japanese(words):
    return ','.join(set([translation_dict.get(word, word) for word in words]))

def detect_food_items(image_path):
    # モデルの読み込み
    model = YOLO('ultralytics/runs/detect/train6/weights/best.pt')

    # 画像に対して推論を実行
    results = model.predict(image_path, save=True, save_txt=True, conf=0.2, iou=0.5)
    names = results[0].names
    classes = results[0].boxes.cls

    # 検出されたクラスIDから食材の名前を取得
    detected_food_names = [names[int(cls)] for cls in classes]

    japanese_words = translate_to_japanese(detected_food_names)

    return japanese_words

# 使用例
image_path = 'ultralytics/predict/2.jpeg'
detected_foods = detect_food_items(image_path)
print(detected_foods)



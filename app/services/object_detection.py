import logging
import sys

sys.path.append("ultralytics")




logger = logging.getLogger(__name__)

TRANSLATION_DICT = {
    "tomato": "トマト",
    "ninnzinn": "にんじん",
    "jyagaimo": "じゃがいも",
    "tamanegi": "玉ねぎ",
    "piimann": "ピーマン",
    "kabocha": "かぼちゃ",
    "nasu": "なす",
    "negi": "ねぎ",
    "daikon": "大根",
    "asuparagasu": "アスパラガス",
    "rennkonn": "れんこん",
    "reatsu": "レタス",
    "satumaimo": "さつまいも",
    "hourennsou": "ほうれん草",
    "kyuuri": "きゅうり",
    "burokkorii": "ブロッコリー",
    "chinngennsai": "青梗菜",
    "toumorokoshi": "とうもろこし",
    "niku": "肉",
    "youguruto": "ヨーグルト",
    "nattou": "納豆",
    "tamago": "卵",
    "kyabetu": "キャベツ",
    "hakusai": "白菜",
}


def translate_to_japanese(words):
    """検出された英語ラベルを日本語に変換する。"""
    return ",".join(
        set([TRANSLATION_DICT.get(word, word) for word in words])
    )



def detect_food_items(image_path):
    """画像から食材を検出し、日本語名のカンマ区切り文字列を返す。"""
    import numpy as np
    from ultralytics import YOLO

    model = YOLO("ultralytics/runs/detect/train6/weights/best.pt")

    results = model.predict(
        image_path, save=True, save_txt=True, conf=0.2, iou=0.5
    )
    names = results[0].names
    classes = results[0].boxes.cls

    detected_food_names = [names[int(cls)] for cls in classes]
    japanese_words = translate_to_japanese(detected_food_names)

    return japanese_words


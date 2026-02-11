import logging

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# モデルとラベルの遅延ロード用キャッシュ
_model = None
_class_names = None


def _load_model():
    """モデルとラベルを遅延ロードする。"""
    global _model, _class_names
    if _model is None:
        from tensorflow.keras.models import load_model as keras_load_model

        _model = keras_load_model("model/new_keras_model.h5", compile=False)
        with open("model/new_labels.txt", "r", encoding="utf-8") as f:
            _class_names = [line.strip() for line in f.readlines()]
    return _model, _class_names


def process_image(image_path):
    """画像を処理し、食材クラスと信頼度スコアを返す。"""
    model, class_names = _load_model()

    image = Image.open(image_path)
    image_resized = image.resize((224, 224))
    if image_resized.mode != "RGB":
        image_resized = image_resized.convert("RGB")

    image_array = np.array(image_resized) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    predictions = model.predict(image_array)
    predicted_class_index = np.argmax(predictions)
    confidence_score = predictions[0][predicted_class_index] * 100

    class_name = class_names[predicted_class_index]
    return class_name, confidence_score

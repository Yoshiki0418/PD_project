from keras.models import load_model
from PIL import Image
import numpy as np

# Load the model
model = load_model("model/keras_model.h5", compile=False)

# Load the labels
with open("model/labels.txt", "r", encoding="utf-8") as file:
    class_names = [line.strip() for line in file.readlines()]

def process_image(image_path):
    # PILを使って画像を読み込み
    image = Image.open(image_path)
    
    # 画像をリサイズし、RGBに変換
    image_resized = image.resize((224, 224))
    if image_resized.mode != 'RGB':
        image_resized = image_resized.convert('RGB')

    # 画像をnumpy配列に変換し、正規化
    image_array = np.array(image_resized) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # 予測を実行
    predictions = model.predict(image_array)
    predicted_class_index = np.argmax(predictions)
    confidence_score = predictions[0][predicted_class_index] * 100

    # クラス名を取得
    class_name = class_names[predicted_class_index]

    return class_name, confidence_score

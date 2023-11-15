from keras.models import load_model
import cv2
import numpy as np

# Load the model
model = load_model("/Users/yamamoto116/Desktop/PD_project/model/keras_model.h5", compile=False)

# Load the labels
with open("/Users/yamamoto116/Desktop/PD_project/model/labels.txt", "r", encoding="utf-8") as file:
    class_names = file.readlines()

def process_image(image_path):
    image = cv2.imread(image_path)

    # Resize the image to (224, 224) pixels
    image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Preprocess the image
    image_resized = np.expand_dims(image_resized, axis=0)
    image_resized = image_resized / 255.0  # Normalize

    # Predict using the model
    predictions = model.predict(image_resized)

    # Get the class index with the highest probability
    predicted_class_index = np.argmax(predictions)
    confidence_score = predictions[0][predicted_class_index] * 100

    # Get the class name and strip the newline character
    class_name = class_names[predicted_class_index].strip()

    return class_name, confidence_score


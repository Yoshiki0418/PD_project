from ultralytics import YOLO
model = YOLO("yolov8l.pt")
model.train(data="dataset.yaml", epochs=100, batch=8, workers=4, degrees=90.0)
from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="/Users/bulusu/Desktop/yolov8/dataset/data.yaml", epochs=100)  # train the model


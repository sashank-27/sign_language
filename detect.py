import cv2
import torch
import numpy as np
from ultralytics import YOLO  # Import YOLOv8 from ultralytics
import time

# Load your custom YOLOv8 model (replace 'best.pt' with the path to your custom model)
model = YOLO('/Users/bulusu/Desktop/yolov8/best.pt')  # Load custom YOLOv8 model

# Setup capture (0 is the default webcam)
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Confidence threshold to filter low-confidence detections
CONFIDENCE_THRESHOLD = 0.5

# For FPS calculation
prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    # Resize frame for faster processing, then scale back for display
    frame_resized = cv2.resize(frame, (640, 480))

    # Perform detection using the custom YOLOv8 model
    results = model(frame_resized)

    # Loop through the detections in the first result
    for result in results:
        for box in result.boxes:  # Iterate through detected bounding boxes
            # Bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())

            # Confidence score
            conf = box.conf[0].cpu().numpy()

            # Class index
            cls = int(box.cls[0].cpu().numpy())

            if conf < CONFIDENCE_THRESHOLD:  # Only proceed if confidence is above the threshold
                continue

            # Get the class label from the model's class names
            label = model.names[cls]
            confidence = f'{conf:.2f}'

            # Draw bounding box
            cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Display label and confidence
            label_text = f'{label}: {confidence}'
            cv2.putText(frame_resized, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Calculate FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Display FPS on the frame
    fps_text = f'FPS: {fps:.2f}'
    cv2.putText(frame_resized, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Show the frame with detections (resize for display purposes)
    cv2.imshow('YOLOv8 Object Detection', cv2.resize(frame_resized, (800, 600)))

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture when everything is done
cap.release()
cv2.destroyAllWindows()

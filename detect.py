from flask import Flask, Response
import cv2
import torch
import time
from ultralytics import YOLO

app = Flask(__name__)

# Load the YOLO model
model = YOLO('best.pt')

CONFIDENCE_THRESHOLD = 0.5

def generate_frames():
    cap = cv2.VideoCapture(0)
    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        frame_resized = cv2.resize(frame, (640, 480))
        results = model(frame_resized)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                conf = box.conf[0].cpu().numpy()
                cls = int(box.cls[0].cpu().numpy())

                if conf < CONFIDENCE_THRESHOLD:
                    continue

                label = model.names[cls]
                confidence = f'{conf:.2f}'

                cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label_text = f'{label}: {confidence}'
                cv2.putText(frame_resized, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        fps_text = f'FPS: {fps:.2f}'
        cv2.putText(frame_resized, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame_resized)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

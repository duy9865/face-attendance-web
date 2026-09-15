import cv2
import os
import json
from datetime import datetime

# ==============================
# ĐƯỜNG DẪN
# ==============================

MODEL_FILE = "data/model/face_model.yml"
ID_MAP_FILE = "data/model/id_map.json"
LABEL_FILE = "data/labels.json"

# ==============================
# KIỂM TRA FILE
# ==============================

if not os.path.exists(MODEL_FILE):
    print("Không tìm thấy mô hình nhận diện!")
    print("Hãy chạy train_model.py trước.")
    exit()

# ==============================
# ĐỌC DỮ LIỆU
# ==============================

with open(ID_MAP_FILE, "r", encoding="utf-8") as file:
    id_map = json.load(file)

with open(LABEL_FILE, "r", encoding="utf-8") as file:
    labels = json.load(file)

# ==============================
# KHỞI TẠO NHẬN DIỆN
# ==============================

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_FILE)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Không thể mở camera!")
    exit()

print("Camera đang chạy.")
print("Nhấn Q để thoát.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("Không đọc được hình ảnh từ camera!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:
        face_image = gray[y:y + h, x:x + w]

        predicted_id, confidence = recognizer.predict(face_image)

        employee_id = id_map.get(str(predicted_id), "")
        employee_name = labels.get(employee_id, "Không xác định")

        # LBPH: confidence càng thấp càng tốt
        if confidence < 70:
            display_name = employee_name
            display_id = employee_id
            color = (0, 255, 0)
        else:
            display_name = "Khong xac dinh"
            display_id = ""
            color = (0, 0, 255)

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            color,
            2
        )

        cv2.putText(
            frame,
            display_name,
            (x, y - 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        if display_id != "":
            cv2.putText(
                frame,
                display_id,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        cv2.putText(
            frame,
            f"Confidence: {confidence:.1f}",
            (x, y + h + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1
        )

    cv2.imshow("Nhan dien khuon mat", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
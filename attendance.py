import cv2
import os
import json
import time

from database import (
    create_tables,
    add_attendance
)


# ==============================
# ĐƯỜNG DẪN
# ==============================

MODEL_FILE = "data/model/face_model.yml"
ID_MAP_FILE = "data/model/id_map.json"
LABEL_FILE = "data/labels.json"


# ==============================
# KHỞI TẠO DATABASE
# ==============================

create_tables()


# ==============================
# KIỂM TRA FILE
# ==============================

if not os.path.exists(MODEL_FILE):
    print("Chưa có mô hình nhận diện!")
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
# KHỞI TẠO MÔ HÌNH
# ==============================

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_FILE)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# ==============================
# MỞ CAMERA
# ==============================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Không thể mở camera!")
    exit()

print("Đưa khuôn mặt vào camera...")


# ==============================
# BIẾN ĐIỀU KHIỂN
# ==============================

attendance_success = False
message = ""
message_color = (0, 255, 0)
message_start_time = 0


# ==============================
# CHẠY CAMERA
# ==============================

while True:
    ret, frame = camera.read()

    if not ret:
        print("Không đọc được camera!")
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

        predicted_id, confidence = recognizer.predict(
            face_image
        )

        employee_id = id_map.get(
            str(predicted_id),
            ""
        )

        employee_name = labels.get(
            employee_id,
            "Khong xac dinh"
        )

        # Confidence càng thấp càng tốt
        if confidence < 70 and employee_id != "":

            color = (0, 255, 0)

            # Chỉ xử lý một lần
            if not attendance_success:

                is_new_attendance = add_attendance(
                    employee_id,
                    employee_name
                )

                if is_new_attendance:
                    message = "DIEM DANH THANH CONG!"
                    message_color = (0, 255, 0)
                else:
                    message = "BAN DA DIEM DANH HOM NAY!"
                    message_color = (0, 255, 255)

                attendance_success = True
                message_start_time = time.time()

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                color,
                2
            )

            cv2.putText(
                frame,
                employee_name,
                (x, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

        else:

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
                "KHONG XAC DINH",
                (x, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    # Hiện thông báo trên camera
    if message != "":
        cv2.putText(
            frame,
            message,
            (35, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            message_color,
            3
        )

    cv2.imshow(
        "He thong diem danh SQLite",
        frame
    )

    # Tự đóng sau 2 giây
    if attendance_success:
        if time.time() - message_start_time >= 2:
            break

    # Nhấn Q để thoát
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ==============================
# ĐÓNG CAMERA
# ==============================

camera.release()
cv2.destroyAllWindows()

print("Hệ thống điểm danh đã đóng.")
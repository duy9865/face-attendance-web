import cv2
import os
import json
import sys

from database import create_tables, add_employee


# ==============================
# XÁC ĐỊNH THƯ MỤC PROJECT
# ==============================

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ==============================
# CẤU HÌNH ĐƯỜNG DẪN
# ==============================

DATA_DIR = os.path.join(
    BASE_DIR,
    "data",
    "faces"
)

LABEL_FILE = os.path.join(
    BASE_DIR,
    "data",
    "labels.json"
)

os.makedirs(
    os.path.dirname(LABEL_FILE),
    exist_ok=True
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

os.makedirs(DATA_DIR, exist_ok=True)

create_tables()


# ==============================
# BỘ PHÁT HIỆN KHUÔN MẶT
# ==============================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# ==============================
# NHẬN THÔNG TIN NHÂN VIÊN
# ==============================

if len(sys.argv) >= 3:
    employee_id = sys.argv[1].strip()
    employee_name = sys.argv[2].strip()
else:
    employee_id = input("Nhập mã nhân viên: ").strip()
    employee_name = input("Nhập tên nhân viên: ").strip()


if employee_id == "" or employee_name == "":
    print("Mã nhân viên và tên không được để trống!")
    sys.exit()


# ==============================
# TẠO THƯ MỤC NHÂN VIÊN
# ==============================

employee_folder = os.path.join(
    DATA_DIR,
    employee_id
)

os.makedirs(employee_folder, exist_ok=True)


# ==============================
# MỞ CAMERA
# ==============================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Không thể mở camera!")
    sys.exit()


sample_count = 0
max_samples = 30

print()
print("Đưa khuôn mặt vào camera.")
print("Chương trình sẽ chụp 30 ảnh.")
print("Nhấn Q để dừng.")
print()


# ==============================
# CHỤP ẢNH KHUÔN MẶT
# ==============================

while True:
    ret, frame = camera.read()

    if not ret:
        print("Không đọc được hình ảnh từ camera!")
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:
        face_image = gray[y:y + h, x:x + w]

        sample_count += 1

        file_path = os.path.join(
            employee_folder,
            f"{sample_count}.jpg"
        )

        cv2.imwrite(
            file_path,
            face_image
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Da chup: {sample_count}/{max_samples}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        if sample_count >= max_samples:
            break

    cv2.imshow(
        "Dang ky khuon mat",
        frame
    )

    key = cv2.waitKey(100) & 0xFF

    if key == ord("q"):
        break

    if sample_count >= max_samples:
        break


# ==============================
# ĐÓNG CAMERA
# ==============================

camera.release()
cv2.destroyAllWindows()


# ==============================
# LƯU THÔNG TIN NHÂN VIÊN
# ==============================

if sample_count > 0:
    if os.path.exists(LABEL_FILE):
        with open(
            LABEL_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            labels = json.load(file)
    else:
        labels = {}

    labels[employee_id] = employee_name

    with open(
        LABEL_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            labels,
            file,
            ensure_ascii=False,
            indent=4
        )

    add_employee(
        employee_id,
        employee_name
    )

    print()
    print(f"Đã đăng ký xong nhân viên: {employee_name}")
    print(f"Mã nhân viên: {employee_id}")
    print(f"Đã lưu {sample_count} ảnh.")
else:
    print()
    print("Chưa chụp được ảnh nào. Không lưu nhân viên.")
import cv2
import os
import json
import numpy as np

# ==============================
# ĐƯỜNG DẪN DỮ LIỆU
# ==============================

FACES_DIR = "data/faces"
MODEL_DIR = "data/model"
MODEL_FILE = os.path.join(MODEL_DIR, "face_model.yml")
LABEL_FILE = "data/labels.json"
ID_MAP_FILE = os.path.join(MODEL_DIR, "id_map.json")

os.makedirs(MODEL_DIR, exist_ok=True)

# Kiểm tra OpenCV có LBPH hay chưa
if not hasattr(cv2, "face"):
    print("OpenCV chưa có cv2.face!")
    print("Hãy cài opencv-contrib-python.")
    exit()

# ==============================
# ĐỌC TÊN NHÂN VIÊN
# ==============================

if not os.path.exists(LABEL_FILE):
    print("Chưa có file data/labels.json")
    print("Hãy đăng ký khuôn mặt trước.")
    exit()

with open(LABEL_FILE, "r", encoding="utf-8") as file:
    labels = json.load(file)

if len(labels) == 0:
    print("Chưa có nhân viên nào được đăng ký.")
    exit()

# ==============================
# CHUẨN BỊ DỮ LIỆU HUẤN LUYỆN
# ==============================

faces = []
face_ids = []

# Ánh xạ ID số sang mã nhân viên
id_map = {}

numeric_id = 0

for employee_id, employee_name in labels.items():
    employee_folder = os.path.join(FACES_DIR, employee_id)

    if not os.path.exists(employee_folder):
        print(f"Không tìm thấy thư mục của {employee_id}")
        continue

    id_map[str(numeric_id)] = employee_id

    image_files = os.listdir(employee_folder)

    for image_file in image_files:
        image_path = os.path.join(employee_folder, image_file)

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            continue

        faces.append(image)
        face_ids.append(numeric_id)

    print(
        f"Đã đọc dữ liệu: {employee_id} - "
        f"{employee_name}"
    )

    numeric_id += 1

if len(faces) == 0:
    print("Không có ảnh khuôn mặt hợp lệ để huấn luyện.")
    exit()

# ==============================
# HUẤN LUYỆN MÔ HÌNH LBPH
# ==============================

print()
print("Đang huấn luyện mô hình...")

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(
    faces,
    np.array(face_ids)
)

recognizer.write(MODEL_FILE)

# Lưu ánh xạ ID
with open(ID_MAP_FILE, "w", encoding="utf-8") as file:
    json.dump(id_map, file, ensure_ascii=False, indent=4)

print()
print("Huấn luyện thành công!")
print(f"Đã lưu mô hình tại: {MODEL_FILE}")
print(f"Đã lưu ánh xạ ID tại: {ID_MAP_FILE}")
print(f"Tổng số ảnh đã học: {len(faces)}")
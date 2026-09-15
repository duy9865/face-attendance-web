from flask import Flask, render_template, request, jsonify
from database import (
    create_tables,
    get_employee_count,
    get_today_attendance_count,
    get_all_employees,
    get_all_attendance
)

import os
import uuid
from datetime import datetime


app = Flask(__name__)

# =========================================================
# CẤU HÌNH
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "web_uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# TRANG DASHBOARD
# =========================================================

@app.route("/")
def index():
    create_tables()

    total_employees = get_employee_count()
    attended_today = get_today_attendance_count()
    employees = get_all_employees()
    attendance_list = get_all_attendance()

    not_attended = total_employees - attended_today

    if not_attended < 0:
        not_attended = 0

    return render_template(
        "index.html",
        total_employees=total_employees,
        attended_today=attended_today,
        not_attended=not_attended,
        employees=employees,
        attendance_list=attendance_list
    )


# =========================================================
# TRANG CHẤM CÔNG BẰNG CAMERA
# =========================================================

@app.route("/cham-cong")
def cham_cong():
    return render_template("cham_cong.html")


# =========================================================
# NHẬN ẢNH TỪ ĐIỆN THOẠI
# =========================================================

@app.route("/upload-face", methods=["POST"])
def upload_face():
    try:
        if "image" not in request.files:
            return jsonify({
                "success": False,
                "message": "Không nhận được ảnh."
            })

        image_file = request.files["image"]

        if image_file.filename == "":
            return jsonify({
                "success": False,
                "message": "Ảnh không hợp lệ."
            })

        filename = (
            datetime.now().strftime("%Y%m%d_%H%M%S")
            + "_"
            + str(uuid.uuid4())[:8]
            + ".jpg"
        )

        save_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        image_file.save(save_path)

        print("Đã nhận ảnh từ điện thoại:")
        print(save_path)

        # =================================================
        # TẠM THỜI:
        # Chưa nhận diện ở bước này.
        # Bước tiếp theo sẽ nối model OpenCV của bạn vào đây.
        # =================================================

        return jsonify({
            "success": True,
            "message": "Đã nhận ảnh thành công.",
            "filename": filename
        })

    except Exception as e:
        print("Lỗi upload ảnh:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        })


# =========================================================
# CHẠY SERVER
# =========================================================

if __name__ == "__main__":
    create_tables()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
        ssl_context="adhoc"
    )
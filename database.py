import sqlite3
import os
from datetime import datetime


# =========================================================
# ĐƯỜNG DẪN DATABASE
# =========================================================

# Lấy thư mục chứa database.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Thư mục data
DATABASE_DIR = os.path.join(BASE_DIR, "data")

# File database
DATABASE_FILE = os.path.join(
    DATABASE_DIR,
    "attendance.db"
)


# =========================================================
# KẾT NỐI DATABASE
# =========================================================

def connect_database():
    """
    Kết nối tới SQLite database.
    Nếu thư mục data chưa tồn tại thì tự tạo.
    """

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    return connection


# =========================================================
# TẠO CÁC BẢNG
# =========================================================

def create_tables():
    """
    Tạo bảng employees và attendance
    nếu chưa tồn tại.
    """

    connection = connect_database()
    cursor = connection.cursor()


    # -----------------------------------------------------
    # BẢNG NHÂN VIÊN
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL
        )
    """)


    # -----------------------------------------------------
    # BẢNG ĐIỂM DANH
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            full_name TEXT NOT NULL,
            attendance_date TEXT NOT NULL,
            attendance_time TEXT NOT NULL,
            status TEXT DEFAULT 'Có mặt'
        )
    """)


    connection.commit()
    connection.close()

    print("Đã tạo database và các bảng thành công!")


# =========================================================
# THÊM NHÂN VIÊN
# =========================================================

def add_employee(employee_id, full_name):
    """
    Thêm nhân viên mới vào database.

    Trả về:
        True  - thêm thành công
        False - mã nhân viên đã tồn tại
    """

    connection = connect_database()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO employees (
                employee_id,
                full_name
            )
            VALUES (?, ?)
        """, (
            employee_id,
            full_name
        ))

        connection.commit()

        print(
            f"Đã thêm nhân viên: "
            f"{employee_id} - {full_name}"
        )

        return True


    except sqlite3.IntegrityError:

        print(
            f"Mã nhân viên "
            f"{employee_id} đã tồn tại!"
        )

        return False


    finally:

        connection.close()


# =========================================================
# LẤY DANH SÁCH NHÂN VIÊN
# =========================================================

def get_all_employees():
    """
    Lấy toàn bộ nhân viên.

    Kết quả dạng:

    [
        ('NV01', 'Nguyen Duy Anh'),
        ('NV02', 'Dang The Nam')
    ]
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            employee_id,
            full_name
        FROM employees
        ORDER BY employee_id
    """)

    employees = cursor.fetchall()

    connection.close()

    return employees


# =========================================================
# ĐẾM TỔNG SỐ NHÂN VIÊN
# =========================================================

def get_employee_count():
    """
    Trả về tổng số nhân viên.
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM employees
    """)

    result = cursor.fetchone()

    connection.close()

    return result[0]


# =========================================================
# KIỂM TRA ĐÃ ĐIỂM DANH HÔM NAY CHƯA
# =========================================================

def has_attended_today(employee_id):
    """
    Kiểm tra nhân viên đã điểm danh hôm nay chưa.

    Trả về:
        True  - đã điểm danh
        False - chưa điểm danh
    """

    today = datetime.now().strftime(
        "%d/%m/%Y"
    )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM attendance
        WHERE employee_id = ?
        AND attendance_date = ?
    """, (
        employee_id,
        today
    ))

    result = cursor.fetchone()

    connection.close()

    return result is not None


# =========================================================
# GHI ĐIỂM DANH
# =========================================================

def add_attendance(employee_id, full_name):
    """
    Ghi nhận điểm danh cho nhân viên.

    Mỗi nhân viên chỉ được điểm danh
    một lần trong ngày.

    Trả về:
        True  - điểm danh thành công
        False - đã điểm danh trước đó
    """

    # -----------------------------------------------------
    # KIỂM TRA ĐÃ ĐIỂM DANH CHƯA
    # -----------------------------------------------------

    if has_attended_today(employee_id):

        print(
            f"{full_name} "
            f"đã điểm danh hôm nay!"
        )

        return False


    # -----------------------------------------------------
    # LẤY NGÀY GIỜ HIỆN TẠI
    # -----------------------------------------------------

    now = datetime.now()

    attendance_date = now.strftime(
        "%d/%m/%Y"
    )

    attendance_time = now.strftime(
        "%H:%M:%S"
    )


    # -----------------------------------------------------
    # GHI VÀO DATABASE
    # -----------------------------------------------------

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO attendance (
            employee_id,
            full_name,
            attendance_date,
            attendance_time,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        employee_id,
        full_name,
        attendance_date,
        attendance_time,
        "Có mặt"
    ))

    connection.commit()
    connection.close()


    print(
        f"Điểm danh thành công: "
        f"{employee_id} - {full_name}"
    )

    return True


# =========================================================
# LẤY TOÀN BỘ LỊCH SỬ ĐIỂM DANH
# =========================================================

def get_all_attendance():
    """
    Lấy toàn bộ lịch sử điểm danh.

    Kết quả:

    (
        employee_id,
        full_name,
        attendance_date,
        attendance_time,
        status
    )
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            employee_id,
            full_name,
            attendance_date,
            attendance_time,
            status
        FROM attendance
        ORDER BY id DESC
    """)

    attendance_list = cursor.fetchall()

    connection.close()

    return attendance_list


# =========================================================
# LẤY ĐIỂM DANH HÔM NAY
# =========================================================

def get_today_attendance():
    """
    Lấy danh sách những người đã điểm danh hôm nay.
    """

    today = datetime.now().strftime(
        "%d/%m/%Y"
    )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            employee_id,
            full_name,
            attendance_date,
            attendance_time,
            status
        FROM attendance
        WHERE attendance_date = ?
        ORDER BY attendance_time DESC
    """, (
        today,
    ))

    attendance_list = cursor.fetchall()

    connection.close()

    return attendance_list


# =========================================================
# ĐẾM SỐ NGƯỜI ĐÃ ĐIỂM DANH HÔM NAY
# =========================================================

def get_today_attendance_count():
    """
    Đếm số nhân viên đã điểm danh hôm nay.
    """

    today = datetime.now().strftime(
        "%d/%m/%Y"
    )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT employee_id)
        FROM attendance
        WHERE attendance_date = ?
    """, (
        today,
    ))

    result = cursor.fetchone()

    connection.close()

    return result[0]


# =========================================================
# LẤY THÔNG TIN NHÂN VIÊN THEO MÃ
# =========================================================

def get_employee_by_id(employee_id):
    """
    Tìm nhân viên theo mã nhân viên.

    Ví dụ:
        get_employee_by_id("NV01")

    Trả về:
        ('NV01', 'Nguyen Duy Anh')

    Nếu không tìm thấy:
        None
    """

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            employee_id,
            full_name
        FROM employees
        WHERE employee_id = ?
    """, (
        employee_id,
    ))

    employee = cursor.fetchone()

    connection.close()

    return employee


# =========================================================
# CHẠY DATABASE.PY TRỰC TIẾP ĐỂ KIỂM TRA
# =========================================================

if __name__ == "__main__":

    print("=" * 50)
    print("KIỂM TRA DATABASE")
    print("=" * 50)

    # Tạo bảng nếu chưa có
    create_tables()

    print()

    # Hiển thị đường dẫn database
    print(
        "Database:",
        DATABASE_FILE
    )

    print()

    # Tổng nhân viên
    print(
        "Tổng số nhân viên:",
        get_employee_count()
    )

    print()

    # Danh sách nhân viên
    print("Danh sách nhân viên:")

    employees = get_all_employees()

    for employee in employees:

        print(
            f" - {employee[0]}: "
            f"{employee[1]}"
        )

    print()

    # Số người điểm danh hôm nay
    print(
        "Đã điểm danh hôm nay:",
        get_today_attendance_count()
    )

    print()

    # Lịch sử điểm danh
    print("Lịch sử điểm danh:")

    attendance_list = get_all_attendance()

    for attendance in attendance_list:

        print(
            f" - {attendance[0]} | "
            f"{attendance[1]} | "
            f"{attendance[2]} | "
            f"{attendance[3]} | "
            f"{attendance[4]}"
        )

    print()

    print("=" * 50)
    print("KIỂM TRA HOÀN TẤT")
    print("=" * 50)
    
    # =====================================================
# SỬA THÔNG TIN NHÂN VIÊN
# =====================================================

def update_employee(employee_id, new_name):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET full_name = ?
        WHERE employee_id = ?
    """, (new_name, employee_id))

    conn.commit()

    updated_rows = cursor.rowcount

    conn.close()

    return updated_rows > 0


# =====================================================
# XÓA NHÂN VIÊN
# =====================================================

def delete_employee(employee_id):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE employee_id = ?
    """, (employee_id,))

    conn.commit()

    deleted_rows = cursor.rowcount

    conn.close()

    return deleted_rows > 0
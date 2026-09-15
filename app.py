import os
import sys
import subprocess
from datetime import datetime

import customtkinter as ctk
from tkinter import dialog, messagebox


# =========================================================
# IMPORT DATABASE
# =========================================================

try:
    from database import (
    create_tables,
    get_all_employees,
    get_employee_count,
    get_all_attendance,
    get_today_attendance_count,
    update_employee,
    delete_employee
)
except Exception as e:
    print("Lỗi import database:", e)


# =========================================================
# ĐƯỜNG DẪN PROJECT
# =========================================================

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================================================
# CẤU HÌNH GIAO DIỆN
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =========================================================
# APP
# =========================================================

class AttendanceApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # -------------------------------------------------
        # KHỞI TẠO DATABASE
        # -------------------------------------------------

        try:
            create_tables()
        except Exception as e:
            print("Không thể khởi tạo database:", e)

        # -------------------------------------------------
        # CẤU HÌNH CỬA SỔ
        # -------------------------------------------------

        self.title("Face Attendance System")
        self.geometry("1200x720")
        self.minsize(1100, 650)

        # -------------------------------------------------
        # MÀU SẮC
        # -------------------------------------------------

        self.bg_color = "#0F172A"
        self.sidebar_color = "#111827"
        self.card_color = "#1E293B"
        self.primary_color = "#2563EB"
        self.success_color = "#16A34A"
        self.warning_color = "#F59E0B"
        self.danger_color = "#DC2626"
        self.text_color = "#F8FAFC"
        self.sub_text_color = "#94A3B8"

        self.configure(fg_color=self.bg_color)

        # -------------------------------------------------
        # GRID CHÍNH
        # -------------------------------------------------

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # -------------------------------------------------
        # TẠO GIAO DIỆN
        # -------------------------------------------------

        self.create_sidebar()
        self.create_main_area()

        # Mở dashboard đầu tiên
        self.show_dashboard()

        # Chạy đồng hồ
        self.update_clock()


    # =====================================================
    # SIDEBAR
    # =====================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color=self.sidebar_color
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)


        # -------------------------------------------------
        # LOGO
        # -------------------------------------------------

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        logo_frame.pack(
            fill="x",
            padx=25,
            pady=(30, 20)
        )


        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="◉",
            font=("Arial", 32, "bold"),
            text_color=self.primary_color
        )

        logo_icon.pack(side="left")


        logo_text_frame = ctk.CTkFrame(
            logo_frame,
            fg_color="transparent"
        )

        logo_text_frame.pack(
            side="left",
            padx=10
        )


        ctk.CTkLabel(
            logo_text_frame,
            text="FACE ATTENDANCE",
            font=("Arial", 14, "bold"),
            text_color=self.text_color
        ).pack(anchor="w")


        ctk.CTkLabel(
            logo_text_frame,
            text="Employee Management",
            font=("Arial", 9),
            text_color=self.sub_text_color
        ).pack(anchor="w")


        # -------------------------------------------------
        # ĐƯỜNG KẺ
        # -------------------------------------------------

        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#273449"
        ).pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )


        # -------------------------------------------------
        # MENU TITLE
        # -------------------------------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="MAIN MENU",
            font=("Arial", 10, "bold"),
            text_color="#64748B"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )


        # -------------------------------------------------
        # MENU
        # -------------------------------------------------

        self.create_menu_button(
            "⌂   Tổng quan",
            self.show_dashboard
        )

        self.create_menu_button(
            "◉   Điểm danh",
            self.run_attendance
        )

        self.create_menu_button(
            "♙   Đăng ký nhân viên",
            self.run_register
        )

        self.create_menu_button(
            "▣   Danh sách nhân viên",
            self.show_employees
        )

        self.create_menu_button(
            "▤   Lịch sử điểm danh",
            self.show_attendance
        )


        # -------------------------------------------------
        # KHOẢNG TRỐNG
        # -------------------------------------------------

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        spacer.pack(
            expand=True,
            fill="both"
        )


        # -------------------------------------------------
        # SYSTEM STATUS
        # -------------------------------------------------

        status_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="#172033",
            corner_radius=12
        )

        status_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )


        ctk.CTkLabel(
            status_frame,
            text="●  SYSTEM STATUS",
            font=("Arial", 10, "bold"),
            text_color=self.success_color
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 4)
        )


        ctk.CTkLabel(
            status_frame,
            text="Face Recognition Ready",
            font=("Arial", 10),
            text_color=self.sub_text_color
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )


        # -------------------------------------------------
        # THOÁT
        # -------------------------------------------------

        exit_button = ctk.CTkButton(
            self.sidebar,
            text="⇥   Thoát hệ thống",
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#7F1D1D",
            text_color="#FCA5A5",
            font=("Arial", 12),
            anchor="w",
            command=self.exit_app
        )

        exit_button.pack(
            fill="x",
            padx=20,
            pady=(0, 25)
        )


    # =====================================================
    # TẠO MENU BUTTON
    # =====================================================

    def create_menu_button(self, text, command):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=46,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#1E293B",
            text_color="#CBD5E1",
            font=("Arial", 12),
            anchor="w",
            command=command
        )

        button.pack(
            fill="x",
            padx=18,
            pady=3
        )


    # =====================================================
    # MAIN AREA
    # =====================================================

    def create_main_area(self):

        self.main = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.bg_color
        )

        self.main.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)


        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        self.header = ctk.CTkFrame(
            self.main,
            height=75,
            corner_radius=0,
            fg_color=self.bg_color
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=35,
            pady=(20, 0)
        )

        self.header.grid_columnconfigure(0, weight=1)


        # HEADER LEFT

        header_left = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )

        header_left.grid(
            row=0,
            column=0,
            sticky="w"
        )


        self.page_title = ctk.CTkLabel(
            header_left,
            text="Tổng quan",
            font=("Arial", 25, "bold"),
            text_color=self.text_color
        )

        self.page_title.pack(anchor="w")


        self.page_description = ctk.CTkLabel(
            header_left,
            text="Quản lý và theo dõi chấm công nhân viên",
            font=("Arial", 11),
            text_color=self.sub_text_color
        )

        self.page_description.pack(
            anchor="w",
            pady=(3, 0)
        )


        # HEADER RIGHT

        header_right = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )

        header_right.grid(
            row=0,
            column=1,
            sticky="e"
        )


        self.clock_label = ctk.CTkLabel(
            header_right,
            text="",
            font=("Arial", 12, "bold"),
            text_color=self.text_color
        )

        self.clock_label.pack(anchor="e")


        ctk.CTkLabel(
            header_right,
            text="● Hệ thống đang hoạt động",
            font=("Arial", 10),
            text_color=self.success_color
        ).pack(anchor="e")


        # -------------------------------------------------
        # CONTENT
        # -------------------------------------------------

        self.content = ctk.CTkScrollableFrame(
            self.main,
            fg_color="transparent"
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=35,
            pady=(10, 30)
        )


    # =====================================================
    # DASHBOARD
    # =====================================================

    def show_dashboard(self):

        self.clear_content()

        self.page_title.configure(
            text="Tổng quan"
        )

        self.page_description.configure(
            text="Quản lý và theo dõi chấm công nhân viên"
        )


        # -------------------------------------------------
        # LẤY DỮ LIỆU THẬT
        # -------------------------------------------------

        try:
            total_employees = get_employee_count()
        except Exception:
            total_employees = 0


        try:
            attended_today = get_today_attendance_count()
        except Exception:
            attended_today = 0


        not_attended = total_employees - attended_today

        if not_attended < 0:
            not_attended = 0


        # -------------------------------------------------
        # WELCOME
        # -------------------------------------------------

        welcome = ctk.CTkFrame(
            self.content,
            fg_color=self.primary_color,
            corner_radius=15,
            height=130
        )

        welcome.pack(
            fill="x",
            pady=(5, 20)
        )

        welcome.pack_propagate(False)


        welcome_text = ctk.CTkFrame(
            welcome,
            fg_color="transparent"
        )

        welcome_text.pack(
            side="left",
            padx=25,
            pady=20
        )


        ctk.CTkLabel(
            welcome_text,
            text="Xin chào! 👋",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(anchor="w")


        ctk.CTkLabel(
            welcome_text,
            text="Chào mừng bạn đến với hệ thống chấm công bằng nhận diện khuôn mặt.",
            font=("Arial", 11),
            text_color="#DBEAFE"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


        # -------------------------------------------------
        # STATISTICS
        # -------------------------------------------------

        stats_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        stats_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)


        self.create_stat_card(
            stats_frame,
            0,
            "NHÂN VIÊN",
            str(total_employees),
            "Tổng số nhân viên",
            "♙"
        )


        self.create_stat_card(
            stats_frame,
            1,
            "CÓ MẶT HÔM NAY",
            str(attended_today),
            "Đã điểm danh",
            "✓"
        )


        self.create_stat_card(
            stats_frame,
            2,
            "CHƯA ĐIỂM DANH",
            str(not_attended),
            "Chưa điểm danh hôm nay",
            "!"
        )


        self.create_stat_card(
            stats_frame,
            3,
            "TRẠNG THÁI",
            "READY",
            "Hệ thống hoạt động",
            "●"
        )


        # -------------------------------------------------
        # QUICK ACTION
        # -------------------------------------------------

        ctk.CTkLabel(
            self.content,
            text="Thao tác nhanh",
            font=("Arial", 18, "bold"),
            text_color=self.text_color
        ).pack(
            anchor="w",
            pady=(5, 12)
        )


        actions = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        actions.pack(
            fill="x",
            pady=(0, 20)
        )

        for i in range(3):
            actions.grid_columnconfigure(i, weight=1)


        self.create_action_card(
            actions,
            0,
            "📷",
            "Điểm danh",
            "Mở camera và nhận diện khuôn mặt",
            self.run_attendance
        )


        self.create_action_card(
            actions,
            1,
            "👤",
            "Đăng ký nhân viên",
            "Thêm nhân viên mới vào hệ thống",
            self.run_register
        )


        self.create_action_card(
            actions,
            2,
            "⚙",
            "Huấn luyện Model",
            "Cập nhật dữ liệu nhận diện",
            self.run_train
        )


        # -------------------------------------------------
        # HOẠT ĐỘNG GẦN ĐÂY
        # -------------------------------------------------

        ctk.CTkLabel(
            self.content,
            text="Hoạt động hệ thống",
            font=("Arial", 18, "bold"),
            text_color=self.text_color
        ).pack(
            anchor="w",
            pady=(5, 12)
        )


        activity = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=12
        )

        activity.pack(fill="x")


        self.create_activity_row(
            activity,
            "✓",
            "Hệ thống đã sẵn sàng",
            "Face Recognition System",
            "Ready"
        )


        self.create_activity_row(
            activity,
            "●",
            f"Database có {total_employees} nhân viên",
            "SQLite Attendance Database",
            "Connected"
        )


        self.create_activity_row(
            activity,
            "●",
            f"Hôm nay đã có {attended_today} lượt điểm danh",
            "Attendance System",
            "Active"
        )


        # NÚT CẬP NHẬT DASHBOARD

        refresh_button = ctk.CTkButton(
            self.content,
            text="↻  Cập nhật dữ liệu",
            height=40,
            corner_radius=8,
            fg_color=self.primary_color,
            hover_color="#1D4ED8",
            command=self.show_dashboard
        )

        refresh_button.pack(
            anchor="e",
            pady=(15, 5)
        )


    # =====================================================
    # STAT CARD
    # =====================================================

    def create_stat_card(
        self,
        parent,
        column,
        title,
        value,
        description,
        icon
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_color,
            corner_radius=12,
            height=130
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5
        )

        card.grid_propagate(False)


        ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 22, "bold"),
            text_color=self.primary_color
        ).place(
            x=18,
            y=15
        )


        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            text_color=self.sub_text_color
        ).place(
            x=55,
            y=18
        )


        ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 25, "bold"),
            text_color=self.text_color
        ).place(
            x=18,
            y=50
        )


        ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 9),
            text_color=self.sub_text_color
        ).place(
            x=18,
            y=92
        )


    # =====================================================
    # ACTION CARD
    # =====================================================

    def create_action_card(
        self,
        parent,
        column,
        icon,
        title,
        description,
        command
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.card_color,
            corner_radius=12,
            height=180
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5
        )

        card.grid_propagate(False)


        ctk.CTkLabel(
            card,
            text=icon,
            font=("Arial", 28)
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 3)
        )


        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 14, "bold"),
            text_color=self.text_color
        ).pack(
            anchor="w",
            padx=18
        )


        ctk.CTkLabel(
            card,
            text=description,
            font=("Arial", 9),
            text_color=self.sub_text_color,
            wraplength=220,
            justify="left"
        ).pack(
            anchor="w",
            padx=18,
            pady=(3, 12)
        )


        ctk.CTkButton(
            card,
            text="Mở chức năng  →",
            height=32,
            corner_radius=6,
            fg_color=self.primary_color,
            hover_color="#1D4ED8",
            font=("Arial", 10, "bold"),
            command=command
        ).pack(
            anchor="w",
            padx=18
        )


    # =====================================================
    # ACTIVITY ROW
    # =====================================================

    def create_activity_row(
        self,
        parent,
        icon,
        title,
        description,
        status
    ):

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=65
        )

        row.pack(
            fill="x",
            padx=15,
            pady=3
        )

        row.pack_propagate(False)


        ctk.CTkLabel(
            row,
            text=icon,
            font=("Arial", 18, "bold"),
            text_color=self.success_color
        ).pack(
            side="left",
            padx=(5, 15)
        )


        text_frame = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )

        text_frame.pack(
            side="left",
            fill="y"
        )


        ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Arial", 11, "bold"),
            text_color=self.text_color
        ).pack(
            anchor="w",
            pady=(10, 0)
        )


        ctk.CTkLabel(
            text_frame,
            text=description,
            font=("Arial", 9),
            text_color=self.sub_text_color
        ).pack(anchor="w")


        ctk.CTkLabel(
            row,
            text=status,
            font=("Arial", 9, "bold"),
            text_color=self.success_color
        ).pack(
            side="right",
            padx=15
        )



    # =====================================================
    # CHẠY CHỨC NĂNG PYTHON / EXE
    # =====================================================

    def run_python_file(
        self,
        filename,
        feature_name,
        employee_id=None,
        employee_name=None
    ):
        try:
            # Khi chạy file .py:
            # BASE_DIR là thư mục chứa app.py
            #
            # Khi chạy file .exe:
            # BASE_DIR là thư mục chứa FaceAttendance.exe

            if getattr(sys, "frozen", False):
                project_dir = os.path.dirname(sys.executable)
            else:
                project_dir = os.path.dirname(
                    os.path.abspath(__file__)
                )

            # Nếu đang chạy EXE thì đổi .py thành .exe
            if getattr(sys, "frozen", False):
                executable_name = os.path.splitext(filename)[0] + ".exe"

                file_path = os.path.join(
                    project_dir,
                    executable_name
                )

                args = [file_path]

            else:
                # Khi chạy bằng Python
                file_path = os.path.join(
                    project_dir,
                    filename
                )

                args = [
                    sys.executable,
                    file_path
                ]

            # Truyền mã và tên nhân viên cho register_face
            if (
                employee_id is not None
                and employee_name is not None
            ):
                args.extend([
                    employee_id,
                    employee_name
                ])

            # Kiểm tra file tồn tại
            if not os.path.exists(file_path):
                messagebox.showerror(
                    "Không tìm thấy chức năng",
                    f"Không tìm thấy file:\n{file_path}"
                )
                return

            # Mở chức năng
            subprocess.Popen(
                args,
                cwd=project_dir,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

        except Exception as e:
            messagebox.showerror(
                "Lỗi",
                f"Không thể mở {feature_name}:\n{e}"
            )

    # =====================================================
    # ĐĂNG KÝ NHÂN VIÊN
    # =====================================================

    def run_register(self):
        dialog = ctk.CTkToplevel(self)

        dialog.title("Đăng ký nhân viên")
        dialog.geometry("450x350")
        dialog.resizable(False, False)

        dialog.transient(self)
        dialog.grab_set()

        title_label = ctk.CTkLabel(
            dialog,
            text="ĐĂNG KÝ NHÂN VIÊN",
            font=("Arial", 22, "bold")
        )
        title_label.pack(pady=(25, 25))

        # =================================================
        # MÃ NHÂN VIÊN
        # =================================================

        ctk.CTkLabel(
            dialog,
            text="Mã nhân viên:",
            font=("Arial", 13)
        ).pack(
            anchor="w",
            padx=40
        )

        employee_id_entry = ctk.CTkEntry(
            dialog,
            width=370,
            height=40,
            placeholder_text="Ví dụ: NV003"
        )
        employee_id_entry.pack(
            pady=(5, 15)
        )

        # =================================================
        # TÊN NHÂN VIÊN
        # =================================================

        ctk.CTkLabel(
            dialog,
            text="Tên nhân viên:",
            font=("Arial", 13)
        ).pack(
            anchor="w",
            padx=40
        )

        employee_name_entry = ctk.CTkEntry(
            dialog,
            width=370,
            height=40,
            placeholder_text="Nhập họ và tên"
        )
        employee_name_entry.pack(
            pady=(5, 20)
        )

    # =====================================================
    # ĐĂNG KÝ NHÂN VIÊN
    # =====================================================

    def run_register(self):
        dialog = ctk.CTkToplevel(self)

        dialog.title("Đăng ký nhân viên")
        dialog.geometry("450x350")
        dialog.resizable(False, False)

        dialog.transient(self)
        dialog.grab_set()

        title_label = ctk.CTkLabel(
            dialog,
            text="ĐĂNG KÝ NHÂN VIÊN",
            font=("Arial", 22, "bold")
        )
        title_label.pack(pady=(25, 25))

        # MÃ NHÂN VIÊN
        ctk.CTkLabel(
            dialog,
            text="Mã nhân viên:",
            font=("Arial", 13)
        ).pack(
            anchor="w",
            padx=40
        )

        employee_id_entry = ctk.CTkEntry(
            dialog,
            width=370,
            height=40,
            placeholder_text="Ví dụ: NV003"
        )
        employee_id_entry.pack(
            pady=(5, 15)
        )

        # TÊN NHÂN VIÊN
        ctk.CTkLabel(
            dialog,
            text="Tên nhân viên:",
            font=("Arial", 13)
        ).pack(
            anchor="w",
            padx=40
        )

        employee_name_entry = ctk.CTkEntry(
            dialog,
            width=370,
            height=40,
            placeholder_text="Nhập họ và tên"
        )
        employee_name_entry.pack(
            pady=(5, 20)
        )

        def start_register():
            employee_id = employee_id_entry.get().strip()
            employee_name = employee_name_entry.get().strip()

            if not employee_id or not employee_name:
                messagebox.showwarning(
                    "Thiếu thông tin",
                    "Vui lòng nhập đầy đủ mã và tên nhân viên.",
                    parent=dialog
                )
                return

            dialog.destroy()

            # Dùng chung hàm chạy file
            self.run_python_file(
                "register_face.py",
                "chức năng đăng ký khuôn mặt",
                employee_id,
                employee_name
            )

        # NÚT MỞ CAMERA
        register_button = ctk.CTkButton(
            dialog,
            text="MỞ CAMERA ĐĂNG KÝ",
            width=250,
            height=42,
            command=start_register
        )
        register_button.pack(pady=10)

        # NÚT HỦY
        cancel_button = ctk.CTkButton(
            dialog,
            text="Hủy",
            width=150,
            height=35,
            fg_color="gray",
            hover_color="#555555",
            command=dialog.destroy
        )
        cancel_button.pack(pady=5)


    # =====================================================
    # HUẤN LUYỆN MODEL
    # =====================================================

    def run_train(self):
        self.run_python_file(
            "train_model.py",
            "chức năng huấn luyện model"
        )


    # =====================================================
    # ĐIỂM DANH
    # =====================================================

    def run_attendance(self):

        self.run_python_file(
            "attendance.py",
            "chức năng điểm danh"
        )


    # =====================================================
    # DANH SÁCH NHÂN VIÊN
    # =====================================================

    def show_employees(self):

        self.clear_content()

        self.page_title.configure(
            text="Danh sách nhân viên"
        )

        self.page_description.configure(
            text="Quản lý thông tin nhân viên trong hệ thống"
        )


        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        top_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        top_frame.pack(
            fill="x",
            pady=(10, 15)
        )


        ctk.CTkLabel(
            top_frame,
            text="Danh sách nhân viên",
            font=("Arial", 20, "bold"),
            text_color=self.text_color
        ).pack(side="left")


        ctk.CTkButton(
            top_frame,
            text="↻ Cập nhật",
            width=120,
            command=self.show_employees
        ).pack(side="right")


        # -------------------------------------------------
        # LẤY DỮ LIỆU DATABASE
        # -------------------------------------------------

        try:
            employees = get_all_employees()
        except Exception as e:

            messagebox.showerror(
                "Lỗi Database",
                f"Không thể đọc danh sách nhân viên:\n{e}"
            )

            employees = []


        # -------------------------------------------------
        # TABLE
        # -------------------------------------------------

        table = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=12
        )

        table.pack(fill="x")


        headers = [
            "STT",
            "MÃ NHÂN VIÊN",
            "HỌ VÀ TÊN",
            "TRẠNG THÁI",
            "THAO TÁC"
        ]


        for column, header in enumerate(headers):

            ctk.CTkLabel(
                table,
                text=header,
                font=("Arial", 10, "bold"),
                text_color=self.sub_text_color
            ).grid(
                row=0,
                column=column,
                padx=20,
                pady=18,
                sticky="w"
            )


        # Không có dữ liệu

        if len(employees) == 0:

            ctk.CTkLabel(
                table,
                text="Chưa có nhân viên nào trong hệ thống",
                font=("Arial", 12),
                text_color=self.sub_text_color
            ).grid(
                row=1,
                column=0,
                columnspan=6,
                padx=20,
                pady=30
            )

            return


        # Hiển thị dữ liệu

        for index, employee in enumerate(employees, start=1):

            employee_id = employee[0]
            full_name = employee[1]


            values = [
                str(index),
                employee_id,
                full_name,
                "Đang hoạt động"
            ]


            for column, value in enumerate(values):

                color = self.text_color

                if column == 3:
                    color = self.success_color


                ctk.CTkLabel(
                    table,
                    text=value,
                    font=("Arial", 11),
                    text_color=color
                ).grid(
                    row=index,
                    column=column,
                    padx=20,
                    pady=14,
                    sticky="w"
                )

                        # Nút sửa
            edit_button = ctk.CTkButton(
                table,
                text="Sửa",
                width=65,
                height=30,
                command=lambda eid=employee_id, name=full_name:
                    self.edit_employee(eid, name)
            )

            edit_button.grid(
                row=index,
                column=4,
                padx=(5, 3),
                pady=10
            )

            # Nút xóa
            delete_button = ctk.CTkButton(
                table,
                text="Xóa",
                width=65,
                height=30,
                fg_color=self.danger_color,
                hover_color="#991B1B",
                command=lambda eid=employee_id, name=full_name:
                    self.remove_employee(eid, name)
            )

            delete_button.grid(
                row=index,
                column=5,
                padx=(3, 10),
                pady=10
            )

        table.grid_columnconfigure(2, weight=1)
        table.grid_columnconfigure(4, weight=0)
        table.grid_columnconfigure(5, weight=0)

# =====================================================
# SỬA THÔNG TIN NHÂN VIÊN
# =====================================================

    def edit_employee(self, employee_id, old_name):
        dialog = ctk.CTkToplevel(self)

        dialog.title("Sửa thông tin nhân viên")
        dialog.geometry("450x300")
        dialog.resizable(False, False)

        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="SỬA THÔNG TIN NHÂN VIÊN",
            font=("Arial", 20, "bold")
        ).pack(pady=(25, 25))

        ctk.CTkLabel(
            dialog,
            text=f"Mã nhân viên: {employee_id}",
            font=("Arial", 13)
        ).pack(pady=5)

        ctk.CTkLabel(
            dialog,
            text="Tên nhân viên mới:",
            font=("Arial", 13)
        ).pack(anchor="w", padx=40, pady=(15, 5))

        name_entry = ctk.CTkEntry(
            dialog,
            width=360,
            height=40
        )
        name_entry.pack()

        name_entry.insert(0, old_name)

        def save_changes():
            new_name = name_entry.get().strip()

            if not new_name:
                messagebox.showwarning(
                    "Thiếu thông tin",
                    "Vui lòng nhập tên nhân viên mới.",
                    parent=dialog
                )
                return

            try:
                success = update_employee(
                    employee_id,
                    new_name
                )

                if success:
                    messagebox.showinfo(
                        "Thành công",
                        "Đã cập nhật thông tin nhân viên.",
                        parent=dialog
                    )

                    dialog.destroy()
                    self.show_employees()

                else:
                    messagebox.showerror(
                        "Lỗi",
                        "Không tìm thấy nhân viên cần sửa.",
                        parent=dialog
                    )

            except Exception as e:
                messagebox.showerror(
                    "Lỗi Database",
                    f"Không thể sửa nhân viên:\n{e}",
                    parent=dialog
                )

        ctk.CTkButton(
            dialog,
            text="LƯU THAY ĐỔI",
            width=220,
            height=40,
            command=save_changes
        ).pack(pady=25)

    # =====================================================
    # XÓA NHÂN VIÊN
    # =====================================================

    def remove_employee(self, employee_id, employee_name):
        confirm = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa nhân viên:\n\n"
            f"Mã: {employee_id}\n"
            f"Tên: {employee_name}\n\n"
            f"Lịch sử điểm danh có thể vẫn còn trong database."
        )

        if not confirm:
            return

        try:
            success = delete_employee(employee_id)

            if success:
                messagebox.showinfo(
                    "Thành công",
                    "Đã xóa nhân viên khỏi database."
                )

                self.show_employees()

            else:
                messagebox.showerror(
                    "Lỗi",
                    "Không tìm thấy nhân viên cần xóa."
                )

        except Exception as e:
            messagebox.showerror(
                "Lỗi Database",
                f"Không thể xóa nhân viên:\n{e}"
            )

    # =====================================================
    # LỊCH SỬ ĐIỂM DANH
    # =====================================================

    def show_attendance(self):

        self.clear_content()

        self.page_title.configure(
            text="Lịch sử điểm danh"
        )

        self.page_description.configure(
            text="Theo dõi lịch sử chấm công của nhân viên"
        )


        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        top_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        top_frame.pack(
            fill="x",
            pady=(10, 15)
        )


        ctk.CTkLabel(
            top_frame,
            text="Lịch sử điểm danh",
            font=("Arial", 20, "bold"),
            text_color=self.text_color
        ).pack(side="left")


        ctk.CTkButton(
            top_frame,
            text="↻ Cập nhật",
            width=120,
            command=self.show_attendance
        ).pack(side="right")


        # -------------------------------------------------
        # LẤY DỮ LIỆU DATABASE
        # -------------------------------------------------

        try:
            attendance_data = get_all_attendance()

        except Exception as e:

            messagebox.showerror(
                "Lỗi Database",
                f"Không thể đọc lịch sử điểm danh:\n{e}"
            )

            attendance_data = []


        # -------------------------------------------------
        # TABLE
        # -------------------------------------------------

        table = ctk.CTkFrame(
            self.content,
            fg_color=self.card_color,
            corner_radius=12
        )

        table.pack(fill="x")


        headers = [
            "MÃ NV",
            "HỌ VÀ TÊN",
            "NGÀY",
            "THỜI GIAN",
            "TRẠNG THÁI"
        ]


        for column, header in enumerate(headers):

            ctk.CTkLabel(
                table,
                text=header,
                font=("Arial", 10, "bold"),
                text_color=self.sub_text_color
            ).grid(
                row=0,
                column=column,
                padx=15,
                pady=18,
                sticky="w"
            )


        # Không có dữ liệu

        if len(attendance_data) == 0:

            ctk.CTkLabel(
                table,
                text="Chưa có lịch sử điểm danh",
                font=("Arial", 12),
                text_color=self.sub_text_color
            ).grid(
                row=1,
                column=0,
                columnspan=5,
                padx=20,
                pady=30
            )

            return


        # Hiển thị dữ liệu

        for row_index, row_data in enumerate(
            attendance_data,
            start=1
        ):

            for column_index, value in enumerate(row_data):

                color = self.text_color

                if column_index == 4:
                    color = self.success_color


                ctk.CTkLabel(
                    table,
                    text=str(value),
                    font=("Arial", 10),
                    text_color=color
                ).grid(
                    row=row_index,
                    column=column_index,
                    padx=15,
                    pady=14,
                    sticky="w"
                )


        table.grid_columnconfigure(1, weight=1)


    # =====================================================
    # XÓA NỘI DUNG CŨ
    # =====================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()


    # =====================================================
    # ĐỒNG HỒ
    # =====================================================

    def update_clock(self):

        now = datetime.now()

        current_time = now.strftime(
            "%d/%m/%Y  |  %H:%M:%S"
        )

        self.clock_label.configure(
            text=current_time
        )

        self.after(
            1000,
            self.update_clock
        )


    # =====================================================
    # THOÁT APP
    # =====================================================

    def exit_app(self):

        answer = messagebox.askyesno(
            "Thoát hệ thống",
            "Bạn có chắc chắn muốn thoát không?"
        )

        if answer:
            self.destroy()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app = AttendanceApp()

    app.mainloop()
import sys
import os
import subprocess


def main():
    if len(sys.argv) < 2:
        print("Thiếu tên file cần chạy.")
        return

    filename = sys.argv[1]

    project_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    file_path = os.path.join(
        project_dir,
        filename
    )

    if not os.path.exists(file_path):
        print(f"Không tìm thấy file: {file_path}")
        return

    subprocess.run(
        [sys.executable, file_path],
        cwd=project_dir
    )


if __name__ == "__main__":
    main()
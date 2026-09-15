
import cv2

# 1. Mở camera laptop
camera = cv2.VideoCapture(0)

# 2. Kiểm tra camera có mở được không
if not camera.isOpened():
    print("Khong the mo camera!")
    exit()

print("Camera da mo thanh cong!")
print("Nhan phim Q de thoat.")

# 3. Vòng lặp đọc hình ảnh từ camera
while True:
    ret, frame = camera.read()

    # Kiểm tra có lấy được hình ảnh không
    if not ret:
        print("Khong doc duoc hinh anh tu camera!")
        break

    # 4. Hiển thị hình ảnh camera
    cv2.imshow("Camera Cham Cong Nhan Vien", frame)

    # 5. Nhấn Q để thoát
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 6. Tắt camera và đóng cửa sổ
camera.release()
cv2.destroyAllWindows()
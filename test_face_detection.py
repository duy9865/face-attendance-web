
import cv2

from core.face_detection import detect_faces


# Mở camera laptop
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Khong the mo camera!")
    exit()

print("Dang phat hien khuon mat...")
print("Nhan Q de thoat.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("Khong doc duoc camera!")
        break

    # Phát hiện tất cả khuôn mặt
    faces = detect_faces(frame)

    # Vẽ khung quanh từng khuôn mặt
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Face",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    # Hiển thị số lượng khuôn mặt
    cv2.putText(
        frame,
        f"So khuon mat: {len(faces)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Phat Hien Khuon Mat", frame)

    # Nhấn Q để thoát
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()
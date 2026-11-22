import cv2
import time

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 10)

if not cap.isOpened():
    print("카메라 연결 실패")
    exit()

print("카메라 연결 성공!")

print("해상도:",
      cap.get(cv2.CAP_PROP_FRAME_WIDTH),
      cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("설정 FPS:", cap.get(cv2.CAP_PROP_FPS))

frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        print("영상 수신 실패")
        break

    frame_count += 1

    if frame_count % 30 == 0:
        elapsed = time.time() - start_time
        print(f"실제 FPS: {frame_count / elapsed:.2f}")

    cv2.imshow("LifeCam HD-3000", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

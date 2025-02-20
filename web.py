import cv2
# 自己的esp32视频流地址
url = 'http://192.168.3.27:9090'

cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Failed to open video stream!")
    exit()

# 设置视频编码器和输出文件
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from video stream!")
        break

    # 调整帧的尺寸
    resized_frame = cv2.resize(frame, (640, 480))

    # 写入调整后的帧到输出文件
    out.write(resized_frame)

    # 显示调整后的帧
    cv2.imshow('frame', resized_frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

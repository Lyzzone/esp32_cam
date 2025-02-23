import cv2
import time

# ESP32-CAM的IP地址和端口号
esp32cam_url = "http://192.168.3.27:5000/video_feed"

# 创建一个VideoCapture对象
cap = cv2.VideoCapture(esp32cam_url)

# 检查是否成功打开视频流
if not cap.isOpened():
    print("无法打开视频流")
    exit()

# 定义保存视频的变量
is_recording = False
out = None
frame_rate = 20.0  # 每秒帧数
video_filename = "output_video.avi"

while True:
    # 读取一帧
    ret, frame = cap.read()

    # 检查是否成功读取帧
    if not ret:
        print("无法读取帧")
        break

    # 显示帧
    cv2.imshow('ESP32-CAM Stream', frame)

    # 如果正在录制，保存帧
    if is_recording:
        out.write(frame)

    # 按下 's' 键开始或停止录制视频
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # 按下 's' 键开始或停止录制
        if not is_recording:
            # 开始录制
            is_recording = True
            out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), frame_rate, (frame.shape[1], frame.shape[0]))
            print("开始录制视频")
        else:
            # 停止录制
            is_recording = False
            out.release()
            print("停止录制视频")

    # 按下 'q' 键退出
    elif key == ord('q'):
        break

# 释放资源
cap.release()
if is_recording:
    out.release()  # 如果视频正在录制，停止时也需要释放资源
cv2.destroyAllWindows()

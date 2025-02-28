import time
import cv2

cap = cv2.VideoCapture(r"elevator.mp4") #导入的视频所在路径
start_time = time.time()
counter = 0 
fps = cap.get(cv2.CAP_PROP_FPS) #视频平均帧率
while cap.isOpened():
    ret, frame = cap.read()
    #键盘输入空格暂停，输入q退出
    key = cv2.waitKey(1) & 0xff
    if key == ord(" "):
        cv2.waitKey(0)
    if key == ord("q"):
        break
    counter += 1#计算帧数
    if (time.time() - start_time) != 0:#实时显示帧数
        cv2.putText(frame, "FPS {0}".format(float('%.1f' % (counter / (time.time() - start_time)))), (500, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                    3)
        cv2.imshow('frame', frame)
        print("FPS: ", counter / (time.time() - start_time))
        counter = 0
        start_time = time.time()
    time.sleep(1 / fps)#按原帧率播放

cap.release()
cv2.destroyAllWindows()

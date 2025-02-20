from microdot import Microdot  # 引入 Microdot 库，用于创建 web 应用
import time  # 引入 time 库，用于时间延迟
import camera  # 引入 camera 库，用于控制摄像头
from machine import reset  # 引入 reset 函数，用于重启设备
import network  # 引入 network 库，用于管理网络连接

# 连接 Wi-Fi 网络的函数
def connect():
    wlan = network.WLAN(network.STA_IF)  # 创建 WLAN 对象，STA_IF 代表站点模式（客户端模式）
    wlan.active(True)  # 激活 Wi-Fi 接口
    if not wlan.isconnected():  # 如果当前没有连接到 Wi-Fi 网络
        print('connecting to network...')  # 打印连接信息
        wlan.connect('door', 'lsw12345678')  # 使用给定的 SSID 和密码连接 Wi-Fi
        while not wlan.isconnected():  # 等待直到连接成功
            pass
    print('network config: ', wlan.ifconfig())  # 打印 Wi-Fi 配置信息


def cam_init():
    # 摄像头初始化部分，最多尝试 5 次
    for i in range(5):
        # 初始化摄像头并设置格式为 JPEG
        cam = camera.init(0, format=camera.JPEG)
        # 设置摄像头分辨率为 HQVGA
        camera.framesize(camera.FRAME_HQVGA)
        # 设置摄像头的图像质量
        camera.quality(10)
        
        print("Camera ready?: ", cam)  # 打印摄像头是否就绪
        if cam:  # 如果摄像头初始化成功
            print("Camera ready")  # 打印摄像头准备好
            break  # 跳出循环
        else:
            time.sleep(2)  # 每次尝试间隔 2 秒
    else:
        print('Timeout')  # 如果在 5 次尝试内没有成功，打印超时
        reset()  # 重启设备

# 调用连接 Wi-Fi 的函数
connect()

# 创建 Microdot 应用实例
app = Microdot()

#启动摄像头
cam_init()

# 根路由，显示 HTML 页面
@app.route('/')
def index(request):
    return '''<!doctype html>
<html>
  <head>
    <title>Microdot Video Streaming</title>
  </head>
  <body>
    <h1>Microdot Video Streaming</h1>
    <img src="/video_feed" width="30%">
  </body>
</html>''', 200, {'Content-Type': 'text/html'}  # 返回一个包含视频流的 HTML 页面

# 视频流路由，处理客户端的视频流请求
@app.route('/video_feed')
def video_feed(request):
    # 返回一个生成器，持续发送视频帧
    def stream():
        yield b'--frame\r\n'  # 视频流的边界标记
        while True:
#             if not request.is_open():  # 如果客户端断开连接
#                 print("Client disconnected, stopping stream.")  # 打印客户端断开连接的信息
#                 break  # 退出循环，结束视频流
            # 捕获一帧图像
            frame = camera.capture()
            # 发送当前帧，使用 multipart/x-mixed-replace 类型进行流式传输
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + \
                b'\r\n--frame\r\n'
            # time.sleep_ms(50)  # 可选的延迟，如果需要减少帧率

    return stream(), 200, {'Content-Type': 'multipart/x-mixed-replace; boundary=frame'}  # 返回视频流响应

@app.get('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return '服务器已经关闭...'

# 主程序入口
if __name__ == '__main__':
    try:
        app.run(debug=True)  # 启动 web 应用，开启调试模式
    except:
        pass  # 捕获异常，防止程序崩溃
    finally:
        camera.deinit()  # 在程序结束时关闭摄像头
        print("Camera deinitialized and program terminated.")  # 打印摄像头已关闭的信息


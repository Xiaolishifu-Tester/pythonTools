import cv2, os, time
from datetime import datetime

#将图像根据手机的摆放方式显示画面
# img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

cv2.namedWindow('camera', cv2.WINDOW_NORMAL) #创建窗口

# 摄像头设置， 使用网络摄像头的URL
video = 'http://admin:admin@192.168.0.201:8081'
capture = cv2.VideoCapture(video)

#初始化保存图像的序号
seral_num = 1

#开始无限循环，直到用户中断
while True:
    success, img = capture.read()
    if not success:
        print("无法抓取帧")
        break

    #将图片旋转90度，竖直显示
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    #显示图像
    cv2.imshow('camera', img)

    #按键处理
    key = cv2.waitKey(10) # 10是毫秒
    if key == 27: # 27是ESC
        break
    # elif key == ord(''):# 空格保存图片
    else:
        img_folder = 'img'
        seral_num = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        img_filename = f"{img_folder}/image_{seral_num}.jpg"
        if key == ord(' ') or key == 115:
            cv2.imwrite(img_filename, img)
            print(f"save image {img_filename}")

# 释放摄像头资源
capture.release()
#关闭窗口
cv2.destroyAllWindows()
import cv2, argparse, glob
import numpy as np


# 鼠标回调函数
def showPixelValue(event, x, y, flags, param):
    global img, combinedResult, placeholder
    if event == cv2.EVENT_MOUSEMOVE:
        # 从鼠标在(X,y)中的位置获取像素值
        bgr = img[y, x]
        # 将BGR像素转换为其他颜色格式
        ycb = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2YCrCb)[0][0]
        lab = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2Lab)[0][0]
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        # 创建一个空占位符来显示值
        placeholder = np.zeros((img.shape[0], 400, 3), dtype=np.uint8)

        cv2.putText(placeholder, "BGR {}".format(bgr), (20, 70), cv2.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
                    cv2.LINE_AA)
        cv2.putText(placeholder, "HSV {}".format(hsv), (20, 140), cv2.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
                    cv2.LINE_AA)
        cv2.putText(placeholder, "YCrCb {}".format(ycb), (20, 210), cv2.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
                    cv2.LINE_AA)
        cv2.putText(placeholder, "LAB {}".format(lab), (20, 280), cv2.FONT_HERSHEY_COMPLEX, .9, (255, 255, 255), 1,
                    cv2.LINE_AA)
        # 将两个结果合并在一个图像中并排显示
        combinedResult = np.hstack([img, placeholder])
        cv2.imshow('PRESS P for Previous,N for Next Image', combinedResult)


if __name__ == '__main__':
    # 加载图像并设置鼠标回调函数
    global img
    files = glob.glob('3.jpg')
    files.sort()
    img = cv2.imread(files[0])
    img = cv2.resize(img, (400, 400))
    cv2.imshow('PRESS P for Previous,N for Next Image', img)
    # 创建一个空窗口
    cv2.namedWindow('PRESS P for Previous,N for Next Image')
    # 为鼠标上的任何事件创建一个回调函数
    cv2.setMouseCallback('PRESS P for Previous,N for Next Image', showPixelValue)
    i = 0
    while (1):
        k = cv2.waitKey(1) & 0xFF
        # 检查文件夹中的下一个图像
        if k == ord('n'):
            i += 1
            img = cv2.imread(files[i % len(files)])
            img = cv2.resize(img, (400, 400))
            cv2.imshow('PRESS P for Previous,N for Next Image', img)
            # 检查文件夹中的前一个图像
        elif k == ord('p'):
            i -= 1
            img = cv2.imread(files[i % len(files)])
            img = cv2.resize(img, (400, 400))
            cv2.imshow('PRESS P for Previous,N for Next Image', img)
        elif k == 27:
            cv2.destroyAllWindows()
            break

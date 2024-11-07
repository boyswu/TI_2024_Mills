import cv2
import numpy as np

# 固定摄像头参数
camera = cv2.VideoCapture(1)


def find_blue_board(image):
    # 转换到HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义绿色的HSV范围
    lower_green= np.array([30, 0, 0])
    upper_green = np.array([110, 100, 150])

    # 创建绿色掩码
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # 闭运算，填充孔洞
    kernel = np.ones((5, 5), np.uint8)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # 闭运算
    # cv2.imshow('Close', mask)     # 显示闭运算结果
    # 开运算，去除孔洞
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # 膨胀运算，扩张孔洞(填充的5*5小方块变大)
    mask = cv2.dilate(mask, kernel, iterations=2)
    # 腐蚀运算，去除小的白色噪声
    mask = cv2.erode(mask, kernel, iterations=2)

    # cv2.imshow('Dilate', mask)  # 显示膨胀运算结果
    # 找到轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到最大的轮廓（假设是棋盘）
    largest_contour = max(contours, key=cv2.contourArea)
    # cv2.drawContours(image, [largest_contour], 0, (0, 255, 0), 2)
    # cv2.imshow('Largest Contour', image)     # 显示最大轮廓
    # 获取最小外接矩形
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)
    box = np.intp(box)
    return box


def opencv_phone():
    global camera
    while True:
        if not camera.isOpened():
            camera.release()
            camera = cv2.VideoCapture(1)
            continue
        ret, image = camera.read()
        if not ret:
            print("读取图像失败")
            camera.release()
            camera = cv2.VideoCapture(1)
            continue

        # 检查图像格式
        if image.shape[2] != 3 or image.dtype != np.uint8:
            print("图像格式错误，请检查图像格式")
            camera.release()
            camera = cv2.VideoCapture(1)
            continue

        photo = cv2.imread("image.jpg")
        # 找到蓝色棋盘的轮廓
        box = find_blue_board(photo)
        # 绘制矩形轮廓
        cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
        # 获取棋盘四个顶点
        board_corners = np.array([box[0], box[1], box[2], box[3]], dtype="float32")
        # 绘制四个顶点
        cv2.circle(image, (int(box[0][0]), int(box[0][1])), 5, (0, 0, 255), -1)
        cv2.circle(image, (int(box[1][0]), int(box[1][1])), 5, (0, 0, 255), -1)
        cv2.circle(image, (int(box[2][0]), int(box[2][1])), 5, (0, 0, 255), -1)
        cv2.circle(image, (int(box[3][0]), int(box[3][1])), 5, (0, 0, 255), -1)
        # 计算棋盘的宽度和高度
        board_width = max(board_corners, key=lambda x: x[0])[0] - min(board_corners, key=lambda x: x[0])[0]
        board_height = max(board_corners, key=lambda x: x[1])[1] - min(board_corners, key=lambda x: x[1])[1]

        # 计算每个小方格的宽度和高度
        square_width = board_width // 3
        square_height = board_height // 3

        # 转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 使用高斯模糊去噪
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 使用霍夫圆变换检测圆形
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=50, param2=30, minRadius=20, maxRadius=50)
        color_move = []
        color_move.clear()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # 检查圆形是否在棋盘范围内
                if min(board_corners, key=lambda x: x[0])[0] <= i[0] <= max(board_corners, key=lambda x: x[0])[0] and \
                        min(board_corners, key=lambda x: x[1])[1] <= i[1] <= max(board_corners, key=lambda x: x[1])[
                    1]:
                    # 提取圆形区域的像素
                    mask = np.zeros(gray.shape, np.uint8)
                    cv2.circle(mask, (i[0], i[1]), i[2], 255, -1)
                    # # 显示掩码
                    # cv2.imshow("mask", mask)


                    # 计算相对位置
                    relative_x = i[0] - min(board_corners, key=lambda x: x[0])[0]
                    relative_y = i[1] - min(board_corners, key=lambda x: x[1])[1]

                    # 计算小方格位置
                    square_x = relative_x // square_width
                    square_y = relative_y // square_height
                    square_index = square_y * 3 + square_x
                    # 计算圆形的颜色
                    mean_val = cv2.mean(image, mask=mask)
                    # 判断是黑棋还是白棋`
                    if mean_val[0] < 128:  # 假设黑色棋子的平均亮度较低
                        color = "black"
                    else:
                        color = "white"

                    # 在图像上标出圆形
                    cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)

                    # 打印在图像上
                    cv2.putText(image, f"{color}, {square_index}", (i[0] - 10, i[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (0, 255, 0), 2)
                    print(f"位置: ({i[0]}, {i[1]}), 颜色: {color}, 对应的小方格位置: {square_index}")

                    atc = (int(square_index), color)

                    color_move.append(atc)
                # 显示结果图像
                cv2.imshow('Detected Circles', image)
                cv2.waitKey(1)
        return color_move


# if __name__ == '__main__':
#     opencv_phone()

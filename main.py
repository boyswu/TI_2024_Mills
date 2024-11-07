import cv2
from ai import tic_tac_toe
from connect_comd import receive_feedback
import threading

# 创建锁
serial_lock = threading.Lock()


def capture_image():
    camera = cv2.VideoCapture(1)

    if not camera.isOpened():
        print("无法打开摄像头")
    else:
        # 读取一帧图像
        ret, frame = camera.read()
        if ret:
            # 成功读取图像，保存为文件
            cv2.imwrite("image.jpg", frame)
            print("已保存图像为 image.jpg")
        else:
            print("读取图像失败")
        camera.release()


def main():
    while True:  # 保证主游戏循环
        capture_image()
        all_move = []
        tic_tac_toe(all_move)
        print("所有落子位置：", all_move)
        print("游戏")

        # 游戏结束后，询问玩家是否继续
        with serial_lock:  # 确保访问串口的安全
            information = receive_feedback()
            if information != 'again':
                print("游戏结束")
                break  # 不再继续游戏则跳出循环


if __name__ == '__main__':
    main_thread = threading.Thread(target=main)
    main_thread.start()

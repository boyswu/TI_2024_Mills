#打开摄像头保存一张图片

import cv2

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
cv2.imwrite('3.jpg', frame)

cap.release()
cv2.destroyAllWindows()


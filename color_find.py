import cv2
import imutils
import numpy as np
import time
def find_largest_quadrilateral(img, img_mask):
    threshold = cv2.GaussianBlur(img_mask, (5,5),0) #размытие

    edges = cv2.Canny(threshold, 25, 250)#контуты
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10)) #устранение мелких обьектов контуров
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    cnts = cv2.findContours(closed, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts) #количество контуров
    total = 0
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 5000:
            continue
        p = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.025 * p, True)

        if len(approx) == 4:
            cv2.drawContours(img, [approx], -1, (0, 255, ), 10)
            total += 1
            print(total)
            #time.sleep(0.1)
    return img,edges
def find_con_by_HSV(img, color, kernel):
    hsv_color = [ [165,  10,   0, 180, 255, 255],  # 0 - красный в сторону синего
                  [  0,  10,   0,  15, 255, 255],  # 1 - красный в сторону зеленого
                  [ 15,  10,   0,  45, 255, 255],  # 2 - желтый
                  [ 45,  10,   0,  75, 255, 255],  # 3 - зеленый
                  [ 75,  10,   0, 105, 255, 255],  # 4 - сиреневый
                  #[105,  10,   0, 135, 255, 255],  # 5 - синий
                  [100, 150, 0, 140, 255, 255],  # 5 - синий свой
                  [135,  10,   0, 165, 255, 255],  # 6 - фиолетовый
                  [  0,   0,   0,   0, 255, 255],  # 7 - черный  ???
                  [  0,  10,   0,   0, 255, 255] ] # 8 - белый   ???
    col = hsv_color[color]
    HSVmin = col[0], col[1], col[2]
    HSVmax = col[3], col[4], col[5]
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_HSV, HSVmin, HSVmax)
    img_Line = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel, kernel), (-1, -1))
    mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, img_Line)

    return mask

def detect_blue_square(frame):#координаты синего квадрата
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            time.sleep(0.1)  
            return (x, y, w, h)

    return None
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hvs = find_con_by_HSV(frame, 5 , 5)
    img,closed = find_largest_quadrilateral(frame, hvs)
    #print(detect_blue_square(frame))
    blue_square = detect_blue_square(frame)
        
    if blue_square:
        x, y, w, h = blue_square
        center_x = x + w // 2
        center_y = y + h // 2
        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2
            
        # Определяем отклонение от центра кадра
        delta_x = center_x - frame_center_x
        delta_y = center_y - frame_center_y
            
        # Двигаем дрон для облета препятствия
        if abs(delta_x) > 50:
            if delta_x > 0:
                print("Движение влево")
            else:
                print("Движение вправо")
            time.sleep(0.1)
    cv2.imshow("oblast", img)
    cv2.imshow("maska", closed)
    cv2.imshow("cvet", hvs)


    if cv2.waitKey(1) == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()

import cv2
import numpy as np
from djitellopy import Tello
import time
from color_find import find_largest_quadrilateral

def avoid_obstacle(tello):
    tello.takeoff()
    time.sleep(2)  # Задержка для стабилизации после взлета
    
    tello.streamon()
    frame_read = tello.get_frame_read()
    
    while True:
        frame = frame_read.frame
        blue_square = find_largest_quadrilateral(frame)
        
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
                    tello.move_left(50)
                else:
                    tello.move_right(50)
                time.sleep(2)
            
            if abs(delta_y) > 50:
                if delta_y > 0:
                    tello.move_down(50)
                else:
                    tello.move_up(50)
                time.sleep(2)
            
            tello.move_forward(100)
            time.sleep(2)
            break  # Завершение цикла после облета препятствия
        
        cv2.imshow('Tello Camera', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    tello.streamoff()
    tello.land()
    cv2.destroyAllWindows()

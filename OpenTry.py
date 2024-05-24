import cv2
import numpy as np
from tkinter import *
import threading

def video_stream():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        frame_flip = cv2.flip(frame, 1)
        try:
            frame_hsv = cv2.cvtColor(frame_flip, cv2.COLOR_BGR2HSV)
            mask_color = cv2.inRange(frame_hsv, low_color, high_color)
            
            result = cv2.bitwise_and(frame_flip, frame_hsv, mask=mask_color)
            
            cv2.imshow('frame', result)
        except:
            cap.release()
            raise
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def update_low_hue(value):
    global low_color
    low_color[0] = value

def update_high_hue(value):
    global high_color
    high_color[0] = value

def update_low_saturation(value):
    global low_color
    low_color[1] = value

def update_high_saturation(value):
    global high_color
    high_color[1] = value

def update_low_value(value):
    global low_color
    low_color[2] = value

def update_high_value(value):
    global high_color
    high_color[2] = value

def tkinter_window():
    root = Tk()
    root.title('Настройки')
    
    # Создание ползунков
    low_hue_slider = Scale(root, from_=0, to=180, orient=HORIZONTAL, label="Low Hue", command=update_low_hue)
    high_hue_slider = Scale(root, from_=0, to=180, orient=HORIZONTAL, label="High Hue", command=update_high_hue)
    low_saturation_slider = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="Low Saturation", command=update_low_saturation)
    high_saturation_slider = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="High Saturation", command=update_high_saturation)
    low_value_slider = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="Low Value", command=update_low_value)
    high_value_slider = Scale(root, from_=0, to=255, orient=HORIZONTAL, label="High Value", command=update_high_value)
    
    # Расположение ползунков на форме
    low_hue_slider.pack()
    high_hue_slider.pack()
    low_saturation_slider.pack()
    high_saturation_slider.pack()
    low_value_slider.pack()
    high_value_slider.pack()
    
    root.mainloop()

# Инициализация значений для low_color и high_color
low_color = np.array((0, 0, 0), np.uint8)
high_color = np.array((0, 20, 0), np.uint8)

# Создание и запуск потоков
video_thread = threading.Thread(target=video_stream)
tkinter_thread = threading.Thread(target=tkinter_window)

video_thread.start()
tkinter_thread.start()
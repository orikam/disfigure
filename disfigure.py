from PIL import Image
from PIL import ImageFilter
from time import time,perf_counter
import numpy as np
import cv2
import pyautogui
import time
import threading

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print("--- %s seconds ---" % (time.time() - start))
        return res
    return wrapper


def screenshoot(pos):
    r = 240
    size = r * 2
    size = int(size)
    print(pos)
    if pos:
        img = pyautogui.screenshot(region=(pos[0] - size//2 ,pos[1]- size // 2, size, size))
    else:
        img = pyautogui.screenshot()
        return img,0 ,0
    return img,pos[0] - size//2 ,pos[1]- size // 2

def get_player(img,pos=None): 
    data = np.array(img)
    size = img.width
    for i in range(0,size,2):
        for j in range(0,size,2):
            if data[i][j][0] > 230 and data[i][j][1] < 20:
                
                return j,i
    return None

def main():
    time.sleep(5)
    pos = None
    found = 10
    img_size = 1920,1080
    while 1:
        img,x_offset,y_offset = screenshoot(pos)
        pos = get_player(img)
        if pos == None:
            found -= 1
            print("--------")
        else:
            pos = pos[0]+x_offset,pos[1]+y_offset
            found = 10
        
        if found == 0:
            #print('++++++')
            break
        if pos: 
            pyautogui.moveTo(pos[0],pos[1])
    
if __name__ == "__main__":
    main()
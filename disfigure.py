from PIL import Image
from PIL import ImageFilter
from time import time,perf_counter
import numpy as np
import cv2
#import pyautogui
import time
import threading
import math

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


class anlys:
    
    def __init__(self,width,hight):
        self.mask = self.create_circular_mask(width,hight)
    def set_img(self,img):
        self.img = img
    def create_circular_mask(self,h, w, center=None, radius=None):
        if center is None: # use the middle of the image
            center = (int(w/2), int(h/2))
        if radius is None: # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w-center[0], h-center[1])

        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

        mask = dist_from_center <= radius
        print(mask.shape)
        return mask
    def calc_treshold_img(self):
        gray_img = self.img.convert("L") 
        gray_data = np.array(gray_img)
        ret,thresh2 = cv2.threshold(gray_data * self.mask,10,255,cv2.THRESH_BINARY_INV)
        self.th_img = thresh2
    def calc_conected_commpent(self):
        self.commpent = cv2.connectedComponentsWithStats(self.th_img * self.mask, 4, cv2.CV_32S)
    def test(self,img):
        data = np.array(img)
        self.calc_treshold_img()
        self.calc_conected_commpent()
        #(numLabels, labels, stats, centroids) = output
        for l in range(0, self.commpent[0]):
            # if this is the first component then we examine the
            # *background* (typically we would just ignore this
            # component in our loop)
            if l == 0:
                text = "examining component {}/{} (background)".format(
                    l + 1, self.commpent[0])
            # otherwise, we are examining an actual connected component
            else:
                text = "examining component {}/{}".format( l + 1, self.commpent[0])
            # print a status message update for the current connected
            # component
            print("[INFO] {}".format(text))
            # extract the connected component statistics and centroid for
            # the current label
            x = self.commpent[2][l, cv2.CC_STAT_LEFT]
            y = self.commpent[2][l, cv2.CC_STAT_TOP]
            w = self.commpent[2][l, cv2.CC_STAT_WIDTH]
            h = self.commpent[2][l, cv2.CC_STAT_HEIGHT]
            area = self.commpent[2][l, cv2.CC_STAT_AREA]
            cX, cY = self.commpent[3][l]
            cv2.rectangle(data, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.circle(data, (int(cX), int(cY)), 4, (0, 0, 255), -1)
        
        cv2.imshow("Output", data)
        cv2.waitKey(0) 
    def log_output(self):
        for l in range(0, self.commpent[0]):
            print(self.commpent[2][l])
            # if this is the first component then we examine the
            # *background* (typically we would just ignore this
            # component in our loop)
            if l == 0:
                text = "examining component {}/{} (background)".format(
                    l + 1, self.commpent[0])
            # otherwise, we are examining an actual connected component
            else:
                text = "examining component {}/{}".format( l + 1, self.commpent[0])
            # print a status message update for the current connected
            # component
            print("[INFO] {}".format(text))
            # extract the connected component statistics and centroid for
            # the current label
            x = self.commpent[2][l, cv2.CC_STAT_LEFT]
            y = self.commpent[2][l, cv2.CC_STAT_TOP]
            w = self.commpent[2][l, cv2.CC_STAT_WIDTH]
            h = self.commpent[2][l, cv2.CC_STAT_HEIGHT]
            area = self.commpent[2][l, cv2.CC_STAT_AREA]
            cX, cY = self.commpent[3][l]
            #cv2.rectangle(data, (x, y), (x + w, y + h), (0, 255, 0), 3)
            #cv2.circle(data, (int(cX), int(cY)), 4, (0, 0, 255), -1)

class target_close:
    def __init__(self):
        pass
    def find_target(self,pos,comp):
        thr = 8
        min_dist = 100000000
        target_center = None
        for i in range(2,comp[0]):
            if comp[2][i, cv2.CC_STAT_WIDTH] > thr and comp[2][i, cv2.CC_STAT_HEIGHT] > thr:
                center = comp[2][i, cv2.CC_STAT_LEFT] + comp[2][i, cv2.CC_STAT_WIDTH] // 2 , comp[2][i, cv2.CC_STAT_TOP] + comp[2][i, cv2.CC_STAT_HEIGHT] // 2
                dist = math.sqrt(pow(pos[0] - center[0],2)+pow(pos[1] - center[1],2))
                if dist < min_dist:
                    min_dist = dist
                    target_center = center
                    print(f'index {i} stats: {comp[2][i]}')
        return target_center

def main():
    time.sleep(5)
    pos = None
    found = 10
    img_size = 1920,1080
    an = None
    ft = target_close()
    while 1:
        img,x_offset,y_offset = screenshoot(pos)
        pos = get_player(img)
        if pos == None:
            found -= 1
            print("--------")
        else:
            if img.width > 500:
                continue
            if an == None:
                an = anlys(480,480)
            an.set_img(img)
            an.calc_treshold_img()
            an.calc_conected_commpent()
            print("++++++")
            an.log_output()
            t = ft.find_target(pos,an.commpent)
            if t != None:
                t = t[0]+x_offset,t[1]+y_offset
            pos = pos[0]+x_offset,pos[1]+y_offset
            found = 10
        
        if found == 0:
            #print('++++++')
            break
        if t: 
            pyautogui.moveTo(t[0],t[1])
    
def test():
    filename = 'img\screen_shot_33.png'
    ft = target_close()
    with Image.open(filename) as img:
        img.load()
        an = anlys(img.width,img.height)
        an.set_img(img)
        an.calc_treshold_img()
        an.calc_conected_commpent()
        #an.test(img)
        t = ft.find_target((img.width,img.height), an.commpent)
        print(f'res = {t},{(img.width//2,img.height//2)}')
        data = np.array(img)
        cv2.rectangle(data, (t[0]-10, t[1] - 10), (t[0]+10, t[1] + 10), (0, 255, 0), 3)
        cv2.imshow("Output", data)
        cv2.waitKey(0) 
        
if __name__ == "__main__":
    test()
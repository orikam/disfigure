from PIL import Image
from PIL import ImageFilter
from time import time,perf_counter
import numpy as np
import cv2

def show_image_from_data(data):
    s = Image.fromarray(data, 'RGB')
    s.show()

def show_image_from_data_gray(data):
    s = Image.fromarray(data, 'L')
    s.show()

filename = 'img\screen_shot_15.png'
with Image.open(filename) as img:
    img.load()
    pos = (0,0)
    for i in range(1):
        start = perf_counter()
        gray_img = img.convert("L") 
        data = np.array(img)
        dataImage = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        gray_data = np.array(gray_img)
        #open_cv_image = data[:, :, ::-1].copy() 
        #grayImage = cv2.cvtColor(data, cv2.COLOR_RGBA2GRAY)
        #data = np.array(gray_img) 
        #print(len(data))
        #data_th = np.where(gray_data < 10, 255, 0)
        #print(f'{type(data_th)}, {type(gray_data)}')
        ret,thresh2 = cv2.threshold(gray_data,10,255,cv2.THRESH_BINARY_INV)
        #show_image_from_data_gray(thresh2)

        output = cv2.connectedComponentsWithStats(thresh2, 4, cv2.CV_32S)
        (numLabels, labels, stats, centroids) = output
        for s in stats:
            print(s)
        print(f'{numLabels}')
        #thresh2.show()
        print(perf_counter() - start)

        
        for l in range(0, numLabels):
            # if this is the first component then we examine the
            # *background* (typically we would just ignore this
            # component in our loop)
            if l == 0:
                text = "examining component {}/{} (background)".format(
                    l + 1, numLabels)
            # otherwise, we are examining an actual connected component
            else:
                text = "examining component {}/{}".format( l + 1, numLabels)
            # print a status message update for the current connected
            # component
            print("[INFO] {}".format(text))
            # extract the connected component statistics and centroid for
            # the current label
            x = stats[l, cv2.CC_STAT_LEFT]
            y = stats[l, cv2.CC_STAT_TOP]
            w = stats[l, cv2.CC_STAT_WIDTH]
            h = stats[l, cv2.CC_STAT_HEIGHT]
            area = stats[l, cv2.CC_STAT_AREA]
            cX, cY = centroids[l]
            cv2.rectangle(dataImage, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.circle(dataImage, (int(cX), int(cY)), 4, (0, 0, 255), -1)
        
        cv2.imshow("Output", dataImage)
        cv2.waitKey(0) 
        
    #for p in range(-10,10):
    #    data[317//2 + p][317//2 + p] = [0, 0,255] 
    s = Image.fromarray(data, 'RGB')
    
#img_res = img.filter(ImageFilter.MaxFilter(3))
#r_edge = r.filter(ImageFilter.FIND_EDGES)
#r_t = r.point(lambda x: 255 if x > 12 else 0)
#img_res = img.filter(ImageFilter.MaxFilter(3)) #0.02
#data = img.getdata() #4.599976819008589e-06
#data = list(img.getdata()) #0.012
#data = np.array(img) #0.0001846999512054026
#running on 317 *317 = 0.0789311999687925
#cv2.imshow("Output", thresh2)
def create_image(name, data):
    name.putdata(data.flatten())
    name.show()


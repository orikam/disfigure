import pyautogui
import time
import threading
#from playsound import playsound

class disfigure:
    def __init__(self):
        self.r = 375


def find_p_faster(pos = None):
    r = 225
    player = None
    size = r * 1.41
    size = int(size)
    target = None
    enemy = []
    if pos: 
        
        img = pyautogui.screenshot(region=(pos[0] - size//2 ,pos[1]- size // 2, size, size))
        
    else:
        img = pyautogui.screenshot()
    start = time.time()
    pix_val = list(img.getdata())
    print("--- %s seconds ---" % (time.time() - start))
    for i,p in enumerate(pix_val):
        if i > img.width * img.height - img.height:
            return player
        if p[0] > 230 and p[1] < 20 and player == None:
            if pos:
                #print(f'{i % img.width} : {i // img.width}')
                player = (pos[0] - size//2 + i % img.width,pos[1] -size // 2 + i // img.width)
            else:
                #print(f'-------------')
                player = (i % img.width, i // img.width)
                
        if pos and target == None:        
            if p[0] < 10 and p[1] < 10 and p[2] < 10:
                cnt = 0
                for q in range(8):
                    if pix_val[i+q][0] < 10 and pix_val[i+q][1] < 10 and pix_val[i+q][2] < 10:
                        cnt+=1
                if cnt == 8:
                    target = (pos[0] - size//2 + i % img.width, pos[1] - size // 2 + i // img.width)
                    #print(f"-++-{target}")
                    pyautogui.moveTo(target[0],target[1])
        if target != None and player != None:
            break
    return player

time.sleep(3)

#find_player(list_colors)
pos = None
found = 10
while 1:
    #start_time = time.time()
    pos = find_p_faster(pos)
    if pos == None:
        found -= 1
    else:
        found = 10
    if found == 0:
        #print('++++++')
        break
    #print(f"======{pos}")
    #print("--- %s seconds ---" % (time.time() - start_time))
    #pyautogui.moveTo(pos[0]+225,pos[1])
#ime.sleep(4)
#--- 0.1556239128112793 seconds ---

#--- 0.17288947105407715 seconds ---

r = 1150 - 775
print(r)
#pyautogui.moveTo(x=1037, y=638)

"""
Point(x=1152, y=535)
Point(x=1037, y=638)
Point(x=944, y=699)
Point(x=770, y=524)
"""

#(254, 61, 67) -idk
import cv2
import numpy as np

def thin_maze_image(folder,name):
    path = folder+'/'+name
    image = cv2.imread(path,0)
    thn = cv2.ximgproc.thinning(image, None, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN) # convert maze image into skeleton using the Zhang-Suen thinning algorithm
    # thn = cv2.ximgproc.thinning(img, None, thinningType=cv2.ximgproc.THINNING_GUOHALL)
    cv2.imwrite(f'{folder}/thinned_{name}', thn)

thin_maze_image('docs/images', 'veryhardmaze.png')

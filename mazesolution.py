import cv2
import numpy as np

# algorithm to find holes in skeleton and fill them with white
def fill_thinned_holes(thn):
    holes = []
    for i in range(1,len(thn)-1):
        for j in range(1,len(thn[i])-1):
            if (thn[i][j] == 0):
                # checks conditions of holes. if it's a hole, record index to fill later.
                if (    (thn[i+1][j] and thn[i][j+1] and not thn[i+1][j+1])
                    or  (thn[i][j-1] and thn[i+1][j] and not thn[i+1][j-1])
                    or  (thn[i-1][j] and thn[i][j+1] and not thn[i-1][j+1])
                    or  (thn[i][j-1] and thn[i-1][j] and not thn[i-1][j-1]) ):
                    holes.append((i,j))
    # now fill all holes white
    for h in holes:
        i, j = h[0], h[1]
        thn[i][j] = 255

def thin_maze_image(folder,name):
    path = folder+'/'+name
    image = cv2.imread(path,0)

    # convert maze image into 1px-wide skeleton using the Zhang-Suen thinning algorithm
    thn = cv2.ximgproc.thinning(image, None, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)

    # algorithm to find holes in skeleton and fill them with white
    # holes typically happen at junctions
    fill_thinned_holes(thn)

    # save thinned and filled image
    cv2.imwrite(f'{folder}/thinned_{name}', thn)

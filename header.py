import numpy as np
import cv2
import imutils

def getArea(image):
    im2, contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    cnt = cnts[0]
    return cv2.contourArea(cnt)

def avaliar(image, vertices):
    mask = np.zeros_like(image)
    if len(mask.shape)==2:
        cv2.fillPoly(mask, vertices, 255)
    else:
        cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension
    return cv2.bitwise_and(image, mask)


def biggest_region(image,frame):
        kernel = np.ones((5,5),np.float32)/25
        cv2.filter2D(image,-1,kernel)
        contours, hierarchy = cv2.findContours(image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
        cnt = cnts[0]
        #cv2.drawContours(frame, [cnt], 0, (255,255,255), 1)
        cv2.drawContours(frame, [cnt], 0, (255,255,255), -1)
        return frame

def negative(imagem):
    imagem = (255-imagem)
    return imagem

def filter_region(image, vertices):
    """
    Create the mask using the vertices and apply it to the input image
    get from https://github.com/naokishibuya/car-finding-lane-lines
    """
    mask = np.zeros_like(image)
    if len(mask.shape)==2:
        cv2.fillPoly(mask, vertices, 255)
    else:
        cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension
    return cv2.bitwise_and(image, mask)


def select_region(image):
    """
    It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
    get from https://github.com/naokishibuya/car-finding-lane-lines
    """
    # first, define the polygon by vertices
    rows, cols = image.shape[:2]
    bottom_left  = [0, rows]
    top_left     = [cols*0.3, rows*0.7]
    bottom_right = [cols, rows]
    top_right    = [cols*0.7, rows*0.7]
    # the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    return filter_region(image, vertices)


# images showing the region of interest only
#sroi_images = list(map(select_region, edge_images))

def skel(image):

    skel = imutils.skeletonize(image, size=(3, 3))
    return skel


import numpy as np
import cv2
import re

def center_image(img, p = 0.35, boolean = True):
    if boolean == False:
        return img
    w, h = img.shape
    cw, ch = w//2, h//2
    #p = 0.4 #max 0.5
    return img[int(cw - w*p): int(cw + w*p), int(ch - h*p) : int(ch + h*p)]

def check_diff(a, b):
    M = max(a, b)
    return abs(a-b)/M

def dist_imgs(a, b, bins = 256):
    hista = cv2.calcHist([a],[0],None,[bins],[0,256]).ravel()
    histb = cv2.calcHist([b],[0],None,[bins],[0,256]).ravel()
    
    hista_n = hista/np.linalg.norm(hista)
    histb_n = histb/np.linalg.norm(histb)
    
    return 1 - check_diff(np.std(hista), np.std(histb))
    #usando std apenas
    return np.max(np.correlate(hista_n, histb_n, "full"))

def matrix_to_chess_notation(array):
    pos1, pos2 = array
    l1, n1 = chr(97 + pos1[1]), 8 - pos1[0]
    l2, n2 = chr(97 + pos2[1]), 8 - pos2[0]
    return ("{}{}{}{}".format(l1, n1, l2, n2), "{}{}{}{}".format(l2, n2, l1, n1))

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]
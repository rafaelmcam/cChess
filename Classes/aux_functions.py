import numpy as np
import cv2
import re
import chess

def center_image(img, boolean = True, p = 0.35):
    if boolean == False:
        return img
    w, h = img.shape
    cw, ch = w//2, h//2
    #p = 0.4 #max 0.5
    return img[int(cw - w*p): int(cw + w*p), int(ch - h*p) : int(ch + h*p)]

def square_color(i, j):
    return ("Black" if (i + j) % 2 else "White")

def test_f1(a, b, threshold = 5):
    a1 = np.sum(cv2.Canny(a, 0, 25))/(255)
    b1 = np.sum(cv2.Canny(b, 0, 25))/(255)
    return (a1 > threshold, b1 > threshold)

def detect_change(a, b, plot = False):
    img1 = center_image(a, p = 0.25)
    img2 = center_image(b, p = 0.25)
    
    if plot:
        fig, axs = plt.subplots(1, 2, figsize = (10, 10))
        axs[0].imshow(cv2.Canny(img1, 0, 25))
        axs[1].imshow(cv2.Canny(img2, 0, 25))

    return test_f1(img1, img2)

def check_diff(a, b):
    M, m = max(a, b), min(a, b)
    return (m/M)


def detect_move(array_geral, jogada):
    matrix = np.zeros((8, 8), dtype = np.uint)
    
    for x in range(8):
        for y in range(8):
            img1 = center_image(array_geral[jogada][x, y], True)
            img2 = center_image(array_geral[jogada+1][x, y], True)
            detected = 1 if check_diff(np.std(img1), np.std(img2)) < 0.5 else 0
#             if detected == 1:
#                 detected = np.sum(detect_change(array_geral[jogada][x, y], array_geral[jogada + 1][x, y])) % 2
            matrix[x, y] = detected
    
    #correct false positives
    for pos in np.transpose(np.nonzero(matrix)):
        if detect_change(array_geral[jogada][pos[0], pos[1]], array_geral[jogada+1][pos[0], pos[1]]) == (False, False):
            matrix[pos[0], pos[1]] = 0
    
    if np.sum(matrix) == 2:
        pass
    elif np.sum(matrix) == 4:
        roque_curto = np.array([1, 1, 1, 1])
        roque_longo = np.array([1, 0, 1, 1, 1])
        if np.array_equal(matrix[0][4:], roque_curto):
            #print("Roque curto Pretas!")
            matrix[0][4:] = np.array([1, 0, 1, 0])
        elif np.array_equal(matrix[7][4:], roque_curto):
            #print("Roque curto Brancas!")
            matrix[7][4:] = np.array([1, 0, 1, 0])
        elif np.array_equal(matrix[0][:5], roque_longo):
            #print("Roque longo Pretas!")
            matrix[0][:5] = np.array([0, 0, 1, 0, 1])
        elif np.array_equal(matrix[7][:5], roque_longo):
            #print("Roque longo Brancas!")
            matrix[7][:5] = np.array([0, 0, 1, 0, 1])
        else:
            print("ERRO na identificação da jogada (sum == 4): {}".format(jogada))
        #print("Roque na jogada: {}.".format(jogada))
        pass
    else:
        print("ERRO na identificação da jogada: {}.".format(jogada))
    
    #correct false positives
    for pos in np.transpose(np.nonzero(matrix)):
        if detect_change(array_geral[jogada][pos[0], pos[1]], array_geral[jogada+1][pos[0], pos[1]]) == (False, True):
            matrix[pos[0], pos[1]] = 2
        elif detect_change(array_geral[jogada][pos[0], pos[1]], array_geral[jogada+1][pos[0], pos[1]]) == (True, True):
            matrix[pos[0], pos[1]] = 2
    return matrix

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]
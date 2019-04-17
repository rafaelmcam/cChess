import matplotlib.pyplot as plt
import numpy as np
import cv2
import chess
import chess.svg
import os
from aux_functions import *

class Game():
    def __init__(self, size = (400, 400)):
        self.aux = np.zeros(size, dtype = np.float32)
        self.pts_aux_square = np.float32([[0,0],[self.aux.shape[1], 0],[self.aux.shape[1],self.aux.shape[0]],[0,self.aux.shape[0]]])

        #self.board = chess.Board()

        self.path_files(path = "../Jogos/1")
        imgInicial = cv2.imread(self.files[0], 0)
        self.calibration(imgInicial)

        self.general_arrays()
        self.movements()
        self.jogo_ate_i()
        return

    def calibration(self, img_calibration):
        points = []
        ix,iy = -1,-1
        img = img_calibration

        def get_points(event,x,y,flags,param):
            global ix, iy, drawing,mode

            if event == cv2.EVENT_LBUTTONDOWN:
                ix,iy = x,y
                #print(x, y)
                points.append([x, y])

        self.img1_r = cv2.resize(img, (int(img.shape[1]/1.4), int(img.shape[0]/1.4)))

        cv2.imshow("click", self.img1_r)
        cv2.setMouseCallback('click', get_points)

        while(1):
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q') or k == 27:
                break
                
        cv2.destroyAllWindows()

        self.pts1 = np.float32(points[:4])
        if len(self.pts1) == 0:
            self.pts1 = np.array([[481., 156.], [852., 158.], [852., 522.], [478., 523.]], dtype = np.float32)
        return

    def path_files(self, path):
        self.files = []
        for r, d, f in os.walk(path):
            for file in f:
                if '.jpg' in file:
                    self.files.append(os.path.join(r, file))
        self.files.sort(key=natural_keys)
        return 

    def general_arrays(self):
        perspectiva = []
        lst_geral = []

        for path in self.files:
            img = cv2.imread(path, 0)
            M = cv2.getPerspectiveTransform(self.pts1, self.pts_aux_square)
            img_r = cv2.resize(img, (int(img.shape[1]/1.4), int(img.shape[0]/1.4)))
            perspectiva.append(cv2.warpPerspective(img_r, M,(self.aux.shape[1],self.aux.shape[0]), self.aux, borderMode = cv2.BORDER_TRANSPARENT))
            lst = []
            for i in range(8):
                for j in range(8):
                    lst.append(perspectiva[-1][perspectiva[-1].shape[1]*i//8:perspectiva[-1].shape[1]*(i+1)//8, perspectiva[-1].shape[0]*j//8:perspectiva[-1].shape[0]*(j+1)//8])
            array = np.array(lst).reshape(8, 8, 50, -1)
            lst_geral.append(array)

        self.array_imgs = np.array(perspectiva)
        self.array_geral = np.array(lst_geral)
        return 

    def movement(self, jogada, use_center = False, p = 0.35):
        array_geral = self.array_geral

        imgs = (jogada-1, jogada)
        lst, two_low = [], []
        
    #     prev = center_image(array_geral[imgs[0]], p = p, boolean = use_center)
    #     curr = center_image(array_geral[imgs[1]], p = p, boolean = use_center)
        
        for i in range(8):
            for j in range(8):
                prev = center_image(array_geral[imgs[0]][i, j], p = p, boolean = use_center)
                curr = center_image(array_geral[imgs[1]][i, j], p = p, boolean = use_center)
                dist_imgs(prev, curr)
                lst.append(dist_imgs(prev, curr))
        lst = np.array(lst).reshape(8, 8)
        
        for i in range(2):
            idx = np.argmin(lst, axis = None) 
            ind = np.unravel_index(idx, lst.shape)

            two_low.append(ind)
        
            lst[ind[0], ind[1]] = 1
        return np.array(two_low)

    def movements(self):
        i = len(self.array_imgs)
        jogadas = []
        for i in range(1, i):
            jogadas.append(self.movement(jogada = i, use_center = False, p = 0.45))
        jogadas = np.array(jogadas)
        self.lst_moves = np.array([matrix_to_chess_notation(x) for x in jogadas])
        return
    
    def debug_step(self, n, pos, center = False, p = 0.35, bins = 256):
        fig, axs = plt.subplots(1, 3, figsize = (20, 6))

        img1 = self.array_geral[n][pos[0], pos[1]]
        img2 = self.array_geral[n+1][pos[0], pos[1]]

        if center == True:
            img1 = center_image(img1, p = p)
            img2 = center_image(img2, p = p)

        h1 = cv2.calcHist([img1],[0],None,[bins],[0,256]).ravel()
        h2 = cv2.calcHist([img2],[0],None,[bins],[0,256]).ravel()


        axs[0].imshow(img1)
        axs[1].imshow(img2)

        axs[2].plot(h1)
        axs[2].plot(h2)

        plt.show()
        return(img1, img2, h1, h2, dist_imgs(img1, img2))

    def push_board(self, move):
        try:
            self.board.push_uci(move[0])
            return
        except:
            try:
                self.board.push_uci(move[1])
                return 
            except:
                print("\n\n\n\n\nErro!\n\n\n\n\n")
                return -1
    def jogo_ate_i(self, i = 9999):
        self.board = chess.Board()
        for jogada in self.lst_moves[:i]:
            self.push_board(jogada)
        return
    
if __name__ == "__main__":
    c = Game()

    print(c.board)
    c.debug_step(0, (4, 3))[-1]

    #print("Img Similarity: ", c.debug_step(0, (4, 3))[-1])


    # cv2.imshow("a", cv2.resize(c.array_imgs[5], (400, 400)))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
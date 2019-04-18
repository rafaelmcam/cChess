import matplotlib.pyplot as plt
import numpy as np
import cv2
import chess
import chess.svg
import os
from aux_functions import *

class Game():
    def __init__(self, size = (400, 400), game_n = 1):
        
        #depois botar as funções que geram os dois arrays abaixo, por enquanto criar nos jupyters e dar load
        self.load_array_geral("../Jogos/{}/array_geral_{}.npy".format(str(game_n), str(game_n)))
        self.load_array_jogadas("../Jogos/{}/array_jogadas_{}.npy".format(str(game_n), str(game_n)))
        return

    def load_array_geral(self, path):
        self.array_geral = np.load(path)

    def load_array_jogadas(self, path):
        self.array_jogadas = np.load(path)

    def show_full_board(self, jogada = 0, center = False, p = 0.35):
        fig, axs = plt.subplots(8, 8, figsize = (10, 10))
        [axi.set_axis_off() for axi in axs.ravel()]
        for i in range(8):
            for j in range(8):
                axs[i, j].imshow(center_image(self.array_geral[jogada][i, j], boolean = center, p = p))
        plt.show()
        return
    
    def detect_move(self, jogada):
        print(detect_move(self.array_geral, jogada))
        return

    def jogo_ate_i(self, i = 9999, print = True):
        self.board = chess.Board()
        for jogada in self.array_jogadas[:i]:
            self.board.push_uci(jogada)
        print(self.board)
        return self.board

    
if __name__ == "__main__":
    c = Game()
    c.jogo_ate_i(2)
 

    #print("Img Similarity: ", c.debug_step(0, (4, 3))[-1])


    # cv2.imshow("a", cv2.resize(c.array_imgs[5], (400, 400)))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
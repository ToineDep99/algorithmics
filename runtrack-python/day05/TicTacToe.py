import pygame, sys
import numpy as np
from pygame.locals import *

###############################################
# PyGame Setup
###############################################

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (8, 144, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
LIGHT_GREY = (230, 230, 230)

# Font object
font = pygame.font.SysFont('Verdana', 60)

# Screen information
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(LIGHT_GREY)
pygame.display.set_caption("TicTacToe1337")

pygame.draw.line(DISPLAYSURF, GREY, (200, 0), (200, 600), 5)
pygame.draw.line(DISPLAYSURF, GREY, (400, 0), (400, 600), 5)
pygame.draw.line(DISPLAYSURF, GREY, (0, 200), (600, 200), 5)
pygame.draw.line(DISPLAYSURF, GREY, (0, 400), (600, 400), 5)

###############################################
# Drawing Functions
###############################################

def drawX(row, col) :
    Y = 100+row*200
    X = 100+col*200
    pygame.draw.polygon(DISPLAYSURF, RED,
                        [(X-20, Y), (X-70, Y-50), (X-50, Y-70),
                         (X, Y-20), (X+50, Y-70), (X+70, Y-50),
                         (X+20, Y), (X+70, Y+50), (X+50, Y+70),
                         (X, Y+20), (X-50, Y+70), (X-70, Y+50)])

def drawO(row, col) :
    Y = 100+row*200
    X = 100+col*200
    pygame.draw.circle(DISPLAYSURF, BLUE, (X, Y), 70)
    pygame.draw.circle(DISPLAYSURF, LIGHT_GREY, (X, Y), 40)

def drawVictory(direction, pos) :
    if direction=='H' :
        pygame.draw.line(DISPLAYSURF, GREEN, (50, 100+pos*200), (550, 100+pos*200), width=30)
    else :
        pygame.draw.line(DISPLAYSURF, GREEN, (100+pos*200, 50), (100+pos*200, 550), width=30)

def tieProtocol() :
    message = font.render("That's a tie", True, BLACK)
    posX = (SCREEN_WIDTH - message.get_width())//2
    posY = (SCREEN_HEIGHT - message.get_height())//2
    DISPLAYSURF.blit(message, (posX, posY))

def winProtocol(player) :
    message1 = font.render("That's a win", True, BLACK)
    message2 = font.render("for "+player, True, BLACK)
    posX1 = (SCREEN_WIDTH - message1.get_width())//2
    posX2 = (SCREEN_WIDTH - message2.get_width())//2
    posY1 = (SCREEN_HEIGHT - (message1.get_height()+message2.get_height()))//2
    posY2 = posY1 + message1.get_height()
    DISPLAYSURF.blit(message1, (posX1, posY1))
    DISPLAYSURF.blit(message2, (posX2, posY2))

###############################################
# TicTacToe Class
###############################################

class TicTacToe() :

    __winning_combinations = [[(0, 0), (0, 1), (0, 2)],
                              [(1, 0), (1, 1), (1, 2)],
                              [(2, 0), (2, 1), (2, 2)],
                              [(0, 0), (1, 0), (2, 0)],
                              [(0, 1), (1, 1), (2, 1)],
                              [(0, 2), (1, 2), (2, 2)],
                              [(0, 0), (1, 1), (2, 2)],
                              [(0, 2), (1, 1), (2, 0)]]

    def __init__(self) :
        self.__board = np.array([[' ' for j in range(3)] for i in range(3)])
        self.__player = 'X'
        self.__last_play = None
    
    def get_board(self) :
        return(self.__board)
    
    def set_board(self, new_board) :
        self.__board = new_board
    
    def print_board(self) :
        print(self.__board)

    def get_player(self) :
        return(self.__player)
    
    def set_player(self, new_player) :
        self.__player = new_player
    
    def switch_player(self) :
        if self.get_player()=='X' :
            self.set_player('O')
        else :
            self.set_player('X')
        print(self.get_player())
    
    def get_last_play(self) :
        return(self.__last_play)
    
    def set_last_play(self, row, col, player) :
        self.__last_play = (row, col, player)
    
    def playable(self, row, col) :
        board = self.get_board()
        return(board[row, col]==' ')

    def play(self, row, col, player) :
        board = self.get_board()
        if self.playable(row, col) :
            board[row, col] = player
            self.set_board(board)
            self.set_last_play(row, col, player)
        else :
            print("Can't play here, play again")
    
    def check_victory(self) :
        board = self.get_board()
        row, col, player = self.get_last_play()
        for comb in self.__winning_combinations :
            if (row, col) in comb :
                cells = [board[r][c] for (r, c) in comb]
                if cells.count(player)==3 :
                    return(True, player)
        return(False, player)
    
    def full_board(self) :
        board = self.get_board()
        return((board!=' ').all())
            
###############################################
# PyGame Loop
###############################################

ttt = TicTacToe()
win = False

while True :
    for event in pygame.event.get() :              
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        if ttt.full_board() and not win :
            tieProtocol()
        if win :
            winProtocol(winner)
        else :
            if event.type == pygame.MOUSEBUTTONDOWN :
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0] :
                    mouse_pos = pygame.mouse.get_pos()
                    row, col = mouse_pos[1]//200, mouse_pos[0]//200
                    player = ttt.get_player()
                    if ttt.playable(row, col) :
                        if player=='X' :
                            drawX(row, col)
                        else :
                            drawO(row, col)
                        ttt.play(row, col, player)
                        ttt.print_board()
                        ttt.set_last_play(row, col, player)
                        win, winner = ttt.check_victory()
                        ttt.switch_player()
    pygame.display.update()




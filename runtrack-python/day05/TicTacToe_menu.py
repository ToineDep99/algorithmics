import pygame, sys
import numpy as np
from pygame.locals import *
import pygame_menu
from pygame_menu.themes import THEME_SOLARIZED
from typing import Optional
from time import sleep

###############################################
# PyGame Setup
###############################################

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
LIGHT_GREY = (230, 230, 230)

# Font object
font = pygame.font.SysFont('Verdana', 40)

# Screen information
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pygame.display.set_caption("TicTacToe1337")

DIFFICULTY = ['EASY']
FIRST_PLAYER = ['player']

###############################################
# Functions
###############################################

def end_bg() :
    DISPLAYSURF.fill((10, 30 ,50))

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

def tieProtocol() :

    global end_menu
    
    end_menu = pygame_menu.Menu('End of the game', width=SCREEN_WIDTH*0.7, height=SCREEN_HEIGHT*0.5, theme=THEME_SOLARIZED)

    end_menu.add.label("THAT'S A TIE !")
    end_menu.add.button('Play again', play_func_jcj)
    end_menu.add.button('Exit to menu', main)

    while True :

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if end_menu.is_enabled():
            end_menu.mainloop(DISPLAYSURF, bgfun=end_bg, fps_limit=FPS)
        
        pygame.display.update()



def winProtocol(player) :

    global end_menu

    end_menu = pygame_menu.Menu('End of the game', width=SCREEN_WIDTH*0.7, height=SCREEN_HEIGHT*0.5, theme=THEME_SOLARIZED)

    end_menu.add.label(f"THAT'S A WIN FOR {player} !")
    end_menu.add.button('Play again', play_func_jcj)
    end_menu.add.button('Exit to menu', main)

    while True :

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if end_menu.is_enabled():
            end_menu.mainloop(DISPLAYSURF, bgfun=end_bg, fps_limit=FPS)
        
        pygame.display.update()

def tieProtocol_ia(difficulty, first_player) :

    global end_menu
    
    end_menu = pygame_menu.Menu('End of the game', width=SCREEN_WIDTH*0.7, height=SCREEN_HEIGHT*0.5, theme=THEME_SOLARIZED)

    end_menu.add.label("THAT'S A TIE !")
    end_menu.add.button('Play again', play_func_IA, difficulty, first_player)
    end_menu.add.button('Exit to menu', main)

    while True :

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if end_menu.is_enabled():
            end_menu.mainloop(DISPLAYSURF, bgfun=end_bg, fps_limit=FPS)
        
        pygame.display.update()



def winProtocol_ia(player, difficulty, first_player) :

    global end_menu

    end_menu = pygame_menu.Menu('End of the game', width=SCREEN_WIDTH*0.7, height=SCREEN_HEIGHT*0.5, theme=THEME_SOLARIZED)

    end_menu.add.label(f"THAT'S A WIN FOR {player} !")
    end_menu.add.button('Play again', play_func_IA, difficulty, first_player)
    end_menu.add.button('Exit to menu', main)

    while True :

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if end_menu.is_enabled():
            end_menu.mainloop(DISPLAYSURF, bgfun=end_bg, fps_limit=FPS)
        
        pygame.display.update()

def set_difficulty(value, diff) :
    DIFFICULTY[0] = diff

def set_first_player(value, player) :
    FIRST_PLAYER[0] = player

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
    
    def get_empty_cells(self) :
        return(np.vstack(np.where(self.get_board()==' ')).T)

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
        print('Setting last play to ', row, col, player)
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
    
    def future_win(self, color) :
        board = self.get_board()
        res = []
        for comb in self.__winning_combinations :
            cells = np.array([board[r, c] for (r, c) in comb])
            if len(np.where(cells==color)[0])==2 and len(np.where(cells==' ')[0])==1 :
                r, c = comb[np.where(cells==' ')[0][0]]
                res.append((r, c))
        return(res)


###############################################
# AI class
###############################################

class AI_easy :

    def __init__(self, color) :
        self.__color = color
    
    def play(self, game) :
        cells = game.get_empty_cells()
        row, col = cells[np.random.choice(cells.shape[0])]
        print(row, col)
        return(row, col)

class AI_medium :
    def __init__(self, color) :
        self.__color = color

    def get_color(self) :
        return(self.__color)

    def play(self, game) :
        ai_color = self.get_color()
        player_color = 'X' if ai_color=='O' else 'O'
        cells = game.future_win(ai_color)
        if len(cells)!=0 :
            return(cells[0])
        cells = game.future_win(player_color)
        if len(cells)!=0 :
            return(cells[0])
        cells = game.get_empty_cells()
        row, col = cells[np.random.choice(cells.shape[0])]
        print(row, col)
        return(row, col)


###############################################
# Play function
###############################################

def play_func_jcj() :

    global main_menu

    ttt = TicTacToe()
    win = False

    main_menu.disable()
    main_menu.full_reset()

    DISPLAYSURF.fill(LIGHT_GREY)

    pygame.draw.line(DISPLAYSURF, GREY, (200, 0), (200, 600), 5)
    pygame.draw.line(DISPLAYSURF, GREY, (400, 0), (400, 600), 5)
    pygame.draw.line(DISPLAYSURF, GREY, (0, 200), (600, 200), 5)
    pygame.draw.line(DISPLAYSURF, GREY, (0, 400), (600, 400), 5)

    while True :
        events = pygame.event.get()
        for event in events :              
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if ttt.full_board() and not win :
                tieProtocol()
                return
            if win :
                winProtocol(winner)
                return
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
                            win, winner = ttt.check_victory()
                            ttt.switch_player()

        pygame.display.update()

def play_func_IA(difficulty, first_player) :

    global main_menu

    ttt = TicTacToe()
    win = False

    main_menu.disable()
    main_menu.full_reset()

    DISPLAYSURF.fill(LIGHT_GREY)

    player_turn = (first_player[0]=='player')
    ai_color = 'O' if player_turn else 'X'
    if difficulty[0]=='EASY' :
        ai = AI_easy(color=ai_color)
    if difficulty[0]=='MEDIUM' :
        ai = AI_medium(color=ai_color)
    if difficulty[0]=='HARD' :
        message1 = font.render("Perfect AI not implemented", True, BLACK)
        message2 = font.render("Launching medium AI", True, BLACK)
        posX1 = (SCREEN_WIDTH - message1.get_width())//2
        posX2 = (SCREEN_WIDTH - message2.get_width())//2
        posY1 = (SCREEN_HEIGHT - (message1.get_height()+message2.get_height()))//2
        posY2 = posY1 + message1.get_height()
        DISPLAYSURF.blit(message1, (posX1, posY1))
        DISPLAYSURF.blit(message2, (posX2, posY2))
        ai = AI_medium(color=ai_color)


    pygame.draw.line(DISPLAYSURF, GREY, (200, 0), (200, 600), 5)
    pygame.draw.line(DISPLAYSURF, GREY, (400, 0), (400, 600), 5)
    pygame.draw.line(DISPLAYSURF, GREY, (0, 200), (600, 200), 5)
    pygame.draw.line(DISPLAYSURF, GREY, (0, 400), (600, 400), 5)
    

    while True :
        events = pygame.event.get()
        for event in events :              
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if ttt.full_board() and not win :
                tieProtocol_ia(difficulty, first_player)
                return
            if win :
                winProtocol_ia(winner, difficulty, first_player)
                return
            else :
                if player_turn :
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
                                win, winner = ttt.check_victory()
                                ttt.switch_player()
                                player_turn = False
                else :
                    player = ttt.get_player()
                    row, col = ai.play(ttt)
                    if ttt.playable(row, col) :
                        if player=='X' :
                            drawX(row, col)
                        else :
                            drawO(row, col)
                        ttt.play(row, col, player)
                        ttt.print_board()
                        win, winner = ttt.check_victory()
                        ttt.switch_player()
                        player_turn = True

        pygame.display.update()

###############################################
# Menu loop
###############################################

def main() :

    global main_menu
    global DISPLAYSURF

    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    IA_menu = pygame_menu.Menu('IA selection', height=SCREEN_HEIGHT, width=SCREEN_WIDTH, theme=THEME_SOLARIZED)

    IA_menu.add.button('Play', play_func_IA, DIFFICULTY, FIRST_PLAYER)
    IA_menu.add.selector('Select difficulty ',
                         [('1 - EASY', 'EASY'),
                          ('2 - MEDIUM', 'MEDIUM'),
                          ('3 - HARD', 'HARD')],
                          onchange=set_difficulty)
    IA_menu.add.selector('Select order of play ',
                         [('Player first', 'player'),
                          ('IA first', 'ia')],
                          onchange=set_first_player)

    main_menu = pygame_menu.Menu('Main menu', height=SCREEN_HEIGHT, width=SCREEN_WIDTH, theme=THEME_SOLARIZED)

    main_menu.add.button('Player vs Player', play_func_jcj)
    main_menu.add.button('Player vs IA', IA_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    while True :
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if main_menu.is_enabled():
            main_menu.mainloop(DISPLAYSURF, fps_limit=FPS)
        
        pygame.display.update()
            
###############################################
# PyGame Loop
###############################################

if __name__ == '__main__':
    main()
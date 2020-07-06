import numpy as np
import pygame
import random


#DEFINE CONSTANTS
BOARD_HEIGHT = 6
BOARD_WIDTH = 7
SQUARE_SIZE = 100
RED = (255,0,0)
BLACK = (0,0,0)
YELLOWISH = (255,200,0)
WHITE = (255,255,255)

player_1 = True
game_over = False

def create_board():
    board = np.zeros((BOARD_HEIGHT,BOARD_WIDTH))
    return board

def check_for_win(board):
    
    global BOARD_HEIGHT, BOARD_WIDTH
    
    #Check for horizontal wins
    for r in range(BOARD_HEIGHT-1,-1,-1):
        for c in range(BOARD_WIDTH-3):
            if board[r][c] != 0:
                if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3]:
                    return board[r][c]  
                
    #Check for vertical wins
    for r in range(BOARD_HEIGHT-1,2,-1):
        for c in range(BOARD_WIDTH):
            if board[r][c] != 0:
                if board[r-1][c] == board[r-2][c] == board[r-3][c] == board[r][c]:
                    return board[r][c]
                
    #Check for diagonal wins
    
    #Lower half positive slope    
    for r in range(5,BOARD_WIDTH-4-1,-1):
        for c in range(3, BOARD_HEIGHT-r-1,-1):
            if board[r][c] != 0:
                if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]:
                    return board[r][c]
                
    #Upper half positive slope
    for r in range(5,BOARD_WIDTH-4-1,-1):
        for c in range(BOARD_HEIGHT-r-1,-1,-1):
            if board[r][c] != 0:
                if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]:
                    return board[r][c]
    
    #Lower half negative slope
    for r in range(BOARD_WIDTH-4):
        for c in range(r+1):
            if board[r][c] != 0:
                if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                    return board[r][c]
    
    #Upper Half positive slope
    for r in range(BOARD_WIDTH-4):
        for c in range(3,r,-1):
            if board[r][c] != 0:
                if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                    return board[r][c]
                
def draw_board(board):
    i = 1
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            pygame.draw.rect(screen,RED,(c*SQUARE_SIZE,r*SQUARE_SIZE + SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.circle(screen,BLACK,(c*SQUARE_SIZE+50,r*SQUARE_SIZE+50+SQUARE_SIZE),45)
            i+=1
            
def update_board(board):
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            if board[r][c] == 1:
                pygame.draw.circle(screen,YELLOWISH,(c*SQUARE_SIZE+50,r*SQUARE_SIZE+50+SQUARE_SIZE),45)
            elif board[r][c] == 2:
                pygame.draw.circle(screen,WHITE,(c*SQUARE_SIZE+50,r*SQUARE_SIZE+50+SQUARE_SIZE),45)
    pygame.display.update()
                

    

board = create_board()

pygame.init()   
screen_width = BOARD_WIDTH * SQUARE_SIZE
screen_height = (BOARD_HEIGHT+1) * SQUARE_SIZE
size = (screen_width,screen_height)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()


while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            break
    
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)
            text = "Player 1" if player_1 else "Player 2"
            col = event.pos[0] // 100 + 1
            #print(col)
            for r in range(BOARD_HEIGHT-1,-1,-1):
                if board[r][col-1] == 0:
                    if player_1:
                        board[r][col-1] = 1
                        player_1 = False                    
                    else:
                        board[r][col-1] = 2
                        player_1 = True
                            
                    #print(board)
                    winner = check_for_win(board)
                    if winner != None:
                        #print(winner)
                        winner_text = "Player 1 Wins!" if winner == 1 else "Player 2 Wins!"
                        pygame.draw.rect(screen,BLACK,(0,0,screen_width,SQUARE_SIZE))
                        pygame.display.update()
                        label = pygame.font.SysFont("Arial",60).render(winner_text,1,WHITE)
                        screen.blit(label,(200,25))
                        game_over = True
                    update_board(board)
                    break        
            
        if event.type == pygame.MOUSEMOTION:
            
            centre = event.pos[0]
            pygame.draw.rect(screen,BLACK,(0,0,screen_width,SQUARE_SIZE))
            if player_1:
                pygame.draw.circle(screen,YELLOWISH,(centre,50),45)
            else:
                pygame.draw.circle(screen,WHITE,(centre,50),45)
            
        pygame.display.update()

if game_over:
    pygame.time.wait(2000)
                
pygame.quit()        
        
        

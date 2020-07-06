import numpy as np
import pygame
import random
import math


#DEFINE CONSTANTS
BOARD_HEIGHT = 6
BOARD_WIDTH = 7
SQUARE_SIZE = 100
PINK = 255,105,180
RED = 255, 0 ,0
ORANGE = (255,165,0)
BLACK = (0,0,0)
YELLOWISH = (0,255,0)
YELLOW = 255,255,0
BLUE = 135,206,235
WHITE = (255,255,255)
WINDOW_LENGTH = 4
start_piece = -1
end_piece = -1

player_1 = random.choice([True,False])
game_over = False

def create_board():
    board = np.zeros((BOARD_HEIGHT,BOARD_WIDTH))
    return board

def check_for_win(board):
    
    global BOARD_HEIGHT, BOARD_WIDTH
    start_piece, end_piece = -1,-1
    winner = None
    #Check for horizontal wins
    for r in range(BOARD_HEIGHT-1,-1,-1):
        for c in range(BOARD_WIDTH-3):
            if board[r][c] != 0:
                if board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3]:
                    start_piece = [r,c]
                    end_piece = [r,c+3]
                    return board[r][c],start_piece, end_piece  
                
    #Check for vertical wins
    for r in range(BOARD_HEIGHT-1,BOARD_HEIGHT-4,-1):
        for c in range(BOARD_WIDTH):            
            if board[r][c] != 0:                
                if board[r-1][c] == board[r-2][c] == board[r-3][c] == board[r][c]:
                    start_piece = [r,c]
                    end_piece = [r-3,c]
                    return board[r][c],start_piece, end_piece
                
    #Check for diagonal wins
    
    #Lower half positive slope    
    for r in range(5,BOARD_WIDTH-4-1,-1):
        for c in range(3, BOARD_HEIGHT-r-1,-1):
            if board[r][c] != 0:
                if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]:
                    start_piece = [r,c]
                    end_piece = [r-3,c+3]
                    return board[r][c],start_piece, end_piece
                
    #Upper half positive slope
    for r in range(5,BOARD_WIDTH-4-1,-1):
        for c in range(BOARD_HEIGHT-r-1,-1,-1):
            if board[r][c] != 0:
                if board[r][c] == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]:
                    start_piece = [r,c]
                    end_piece = [r-3,c+3]
                    return board[r][c],start_piece, end_piece
    
    #Lower half negative slope
    for r in range(BOARD_WIDTH-4):
        for c in range(r+1):
            if board[r][c] != 0:
                if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                    start_piece = [r,c]
                    end_piece = [r+3,c+3]
                    return board[r][c],start_piece, end_piece
    
    #Upper Half positive slope
    for r in range(BOARD_WIDTH-4):
        for c in range(3,r,-1):
            if board[r][c] != 0:
                if board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                    start_piece = [r,c]
                    end_piece = [r+3,c+3]
                    return board[r][c],start_piece, end_piece
    return winner,start_piece,end_piece
                
def isTerminalNode(board):
    winner,a,b = check_for_win(board)
    return winner != None or len(getValidColumns(board)) == 0
                
def minimax(board,depth,maximizingPlayer,alpha,beta):
    #print("CC")
    if depth == 0 or isTerminalNode(board):
        if isTerminalNode(board):
            winner,a,b = check_for_win(board)
            if winner == 1:
                return (-100000000000000000000,None)
            elif winner == 2:
                return (100000000000000000000,None)
            else:
                return (0,None)
        else:
            return scoring_io(board,2),None
    if maximizingPlayer:
        best_score = -math.inf
        best_col = random.choice(getValidColumns(board))
        for column in getValidColumns(board):
            temp_board = board.copy()
            drop_piece(temp_board,2,column,False)
            score = minimax(temp_board,depth-1,False,alpha,beta)[0]
            if score > best_score:
                best_score = score
                best_col = column
            alpha = max(score,alpha)
            if alpha>= beta:
                break
        return best_score,best_col
    else:
        best_score = math.inf
        best_col = random.choice(getValidColumns(board))
        for column in getValidColumns(board):
            temp_board = board.copy()
            drop_piece(temp_board,1,column,True)
            score = minimax(temp_board,depth-1,True,alpha,beta)[0]
            
            if score < best_score:
                best_score = score
                best_col = column
            beta = min(score,beta)
            if beta <= alpha:
                break
        return best_score,best_col
                
def scoring_function(window,piece):
    score = 0
    
    opp_piece = 1 if piece == 2 else 2
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4
    return score
    
                
def scoring_io(board,piece):   
    score = 0
    
    #Scoring Centre
    centre_col = list(board[:,BOARD_WIDTH//2])
    centre_count = centre_col.count(piece)
    score += 6*centre_count
    
    #Horizontal Windows    
    for r in range(BOARD_HEIGHT-1,-1,-1):        
        row = list(board[r,:])        
        for c in range(BOARD_WIDTH-3):
            window = row[c:c+WINDOW_LENGTH]
            score += scoring_function(window,piece)
            
    #Vertical Windows
    for c in range(BOARD_WIDTH):        
        col = list(board[:,c])        
        for r in range(BOARD_HEIGHT-1,BOARD_HEIGHT-4,-1):
            window = col[r:r+WINDOW_LENGTH]
            score += scoring_function(window,piece)
            
    #Diagonal Windows
    for r in range(5,BOARD_WIDTH-4-1,-1):
        for c in range(3, BOARD_HEIGHT-r-1,-1):
            window = [board[r-i][c+i] for i in range(WINDOW_LENGTH)]
            score += scoring_function(window,piece)
            
    for r in range(5,BOARD_WIDTH-4-1,-1):
        for c in range(BOARD_HEIGHT-r-1,-1,-1):
            window = [board[r-i][c+i] for i in range(WINDOW_LENGTH)]
            score += scoring_function(window,piece)
    
    for r in range(BOARD_WIDTH-4):
        for c in range(r+1):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += scoring_function(window,piece)
            
    for r in range(BOARD_WIDTH-4):
        for c in range(3,r,-1):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += scoring_function(window,piece)            
            
    return score
            
def make_best_move(board,piece):
    valid_columns = getValidColumns(board)
    best_score = -math.inf
    best_col = random.choice(valid_columns)
    for c in valid_columns:
        temp_board = board.copy()
        drop_piece(temp_board,piece,c,False)
        score = scoring_io(temp_board,piece)
        
        if score > best_score:
            best_score = score
            best_col = c
    return best_col
        

def isValidColumn(board,col):
    return board[0][col] == 0
    
def getValidColumns(board):
    validColumns = []
    
    for c in range(BOARD_WIDTH):
        if isValidColumn(board,c):
            validColumns.append(c)
    return validColumns
       
    
                
def draw_board(board):
    
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            pygame.draw.rect(screen,BLUE,(c*SQUARE_SIZE,r*SQUARE_SIZE + SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.circle(screen,BLACK,(c*SQUARE_SIZE+50,r*SQUARE_SIZE+50+SQUARE_SIZE),45)
            
            
def update_board(board,start_piece,end_piece):
    for r in range(BOARD_HEIGHT):
        for c in range(BOARD_WIDTH):
            if board[r][c] == 1:
                pygame.draw.circle(screen,PINK,(c*SQUARE_SIZE+50,r*SQUARE_SIZE+50+SQUARE_SIZE),45)
                pygame.display.update()
            elif board[r][c] == 2:
                pygame.draw.circle(screen,YELLOW,(c*SQUARE_SIZE+50,r*SQUARE_SIZE+50+SQUARE_SIZE),45)
                pygame.display.update()
                
    if start_piece != -1 and end_piece != -1:
        line_start = ((start_piece[1])*SQUARE_SIZE+50,(start_piece[0]+1)*SQUARE_SIZE+50)
        line_end = ((end_piece[1])*SQUARE_SIZE+50,(end_piece[0]+1)*SQUARE_SIZE+50)
        pygame.draw.line(screen,BLACK,line_start,line_end,5)
        pygame.display.flip()
    
    
                

def drop_piece(board,piece,col,player_1):
    if player_1:
        piece = 1
    else:
        piece = 2
    for r in range(BOARD_HEIGHT-1,-1,-1):
        if board[r][col] == 0:
            board[r][col] = piece
            break
    

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
            text = "Player 1" if player_1 else "Player 2"
                        
            col = event.pos[0] // 100
            if isValidColumn(board,col):
                drop_piece(board,1,col,player_1)
                player_1 = False
                update_board(board,start_piece,end_piece)
                               

            winner,start_piece,end_piece = check_for_win(board)
            if winner != None:
                winner_text = "Player 1 Wins!" if winner == 1 else "Player 2 Wins!"
                pygame.draw.rect(screen,BLACK,(0,0,screen_width,SQUARE_SIZE))
                pygame.display.update()
                label = pygame.font.SysFont("Arial",60).render(winner_text,1,WHITE)
                screen.blit(label,(200,25))
                game_over = True
            update_board(board,start_piece,end_piece)
            break
        
        if len(getValidColumns(board)) == 0:
            label = pygame.font.SysFont("Arial",60).render("No More Moves!",1,WHITE)
            screen.blit(label,(200,25))
            game_over = True
        
        if not player_1 and not game_over:        
            #num = make_best_move(board,2) -----> equivalent to 0 depth minimax
            score,num = minimax(board,4,True,-math.inf,math.inf)
            if isValidColumn(board,num):
                drop_piece(board,2,num,player_1)
                player_1 = True        
                #pygame.time.wait(500) --------> For Delay, not required when using minimax
    
            winner,start_piece,end_piece = check_for_win(board)
            if winner != None:
                winner_text = "You Win!" if winner == 1 else "AI Wins!"
                pygame.draw.rect(screen,BLACK,(0,0,screen_width,SQUARE_SIZE))
                pygame.display.update()
                label = pygame.font.SysFont("Arial",60).render(winner_text,1,WHITE)
                screen.blit(label,(250,25))
                game_over = True
            update_board(board,start_piece,end_piece)
            break
            
            
        if event.type == pygame.MOUSEMOTION:
            
            centre = event.pos[0]
            pygame.draw.rect(screen,BLACK,(0,0,screen_width,SQUARE_SIZE))
            if player_1:
                pygame.draw.circle(screen,PINK,(centre,50),45)
            
        pygame.display.update()

if game_over:
    pygame.time.wait(5000)
                
pygame.quit()        
        
        

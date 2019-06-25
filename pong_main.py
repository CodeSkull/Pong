'''
Created on Aug 28, 2017

@author: Julian
'''
import pygame, sys
from pygame.locals import *

# Number of frames per second
# Change this value to speed up or slow down the game
FPS = 200

WINDOWWIDTH =  400
WINDOWHEIGHT = 300
LINETHICKNESS = 10 # thickness of lines
PADDLESIZE = 50 # length of the paddle
PADDLEOFFSET = 20 # the distance the paddle is from the edges

# Set up the colours
BLACK = (0    ,0    ,0  )
WHITE = (255  ,255  ,255)

# Draws the arena the game will be played in
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    # Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS*2)
    # Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, (int((WINDOWWIDTH/2)),0), (int((WINDOWWIDTH/2)),WINDOWHEIGHT), int(LINETHICKNESS/4))

# Draws the paddle
def drawPaddle(paddle):
    # Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    # Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    # Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

# Draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

# Moves the ball
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

# Checks for a collision with a wall, and 'bounces' ball off it
# Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

# Checks if the ball has hit a paddle, and 'bounces' ball off it
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
        return 1

# Checks to see if a point has been scored & returns new score
def checkPointScored(paddle, ball, score, ballDirX, x):
    # reset points if left wall is hit
    if ball.left == LINETHICKNESS and x == 1:
        score += 1
        return score
    elif ball.right == (WINDOWWIDTH - LINETHICKNESS) and x == 2:
        score += 1
        return score
    # if no points scored, return score unchanged
    else:
        return score
    '''
    # +1 point for hitting the ball
    elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        score += 1
        return score
    # +5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score
        '''
    

# Displays the current score on the screen
def displayScore(score, x):
    resultSurf = BASICFONT.render('%s' %str(score), True, WHITE) #creates new surface
    resultRect = resultSurf.get_rect()
    if x == 1:
        resultRect.topleft = (WINDOWWIDTH/2 + 50, 25)
    elif x == 2:
        resultRect.topleft = (WINDOWWIDTH/2 - 50, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

# "Artificial Intelligence" of computer player
# Returns position of the paddle
def artificialIntelligence(ball, ballDirX, paddle2):
    # If ball is moving away from paddle, center bat
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT/2): # paddle2.centery - used to find the center of the paddle
            paddle2.y += 1
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -= 1
    # If ball moving towards bat, track its movement
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2

def main():
    pygame.init()

    # Creates a main surface that will be used throughout the program
    global DISPLAYSURF
    ## Font Information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # Titlte of the window
    pygame.display.set_caption("Pong")

    # Initiate variable and set starting positions
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2
    score1 = 0
    score2 = 0

    # Keeps track of ball direction
    ballDirX = -1 ## left = -1 | right = 1
    ballDirY = -1 ## up = -1 | down = 1

    # Creates rectangles for ball and paddles
    # format for creating a rectangle - pygame.Rect(x coor, y coor, width of rect, len of rect)
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    # Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0) # makes cursor invisible in the window
    
    while True:  #main game loop, will keep running until the game is quit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
        
        #input for player 2
        keys = pygame.key.get_pressed() # checking pressed keys
        if keys[pygame.K_UP]:
            paddle2.y -= 2
        elif keys[pygame.K_DOWN]:
            paddle2.y += 2

        # To ensure game is updated every tick or FPS
        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        #paddle2 = artificialIntelligence(ball, ballDirX, paddle2)
        score1 = checkPointScored(paddle1, ball, score1, ballDirX, 1)
        score2 = checkPointScored(paddle2, ball, score2, ballDirX, 2)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)

        displayScore(score1, 1)
        displayScore(score2, 2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()

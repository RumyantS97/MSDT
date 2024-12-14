import random
import copy
import logging
from tkinter import *


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('msdt-4/logs.txt', encoding='utf-8')
    ]
)


def init():
    logging.info("initializing the game")
    printInstructions()
    canvas.data.isGameOver = False 
    board = []
    canvas.data.emptyColor = "blue"
    for x in range(canvas.data.rows):
        board.append([canvas.data.emptyColor]*canvas.data.cols)
    canvas.data.tetrisBoard = board
    tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
    canvas.data.tetrisPieces = tetrisPieces()
    canvas.data.tetrisPieceColors = tetrisPieceColors
    canvas.data.score = 0
    newFallingPiece()
    redrawAll()
    logging.info("game initialized")
    
def printInstructions():
    print("Welcome to Tetris!")
    print("Use the arrow keys to move Left, Right, and Down.")
    print("Press Up to rotate counter-clockwise")
    print("Press 'r' to restart.")
    print("Press 'q' to end the game.")

def tetrisPieces():
    iPiece = [[ True,  True,  True,  True]]
    jPiece = [[ True, False, False ],[ True, True,  True]]
    lPiece = [[ False, False, True],[ True,  True,  True]]
    oPiece = [[ True, True],[ True, True]]
    sPiece = [[ False, True, True],[ True,  True, False ]]
    tPiece = [[ False, True, False ],[ True,  True, True]]
    zPiece = [[ True,  True, False ],[ False, True, True]]
    tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]    
    return tetrisPieces

def newFallingPiece():
    pieceIndex = random.randint(0, len(canvas.data.tetrisPieces) - 1)
    colorIndex = random.randint(0, len(canvas.data.tetrisPieceColors) - 1)
    #Use random function to place tetris piece at random location
    
    canvas.data.fallingPiece = canvas.data.tetrisPieces[pieceIndex]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[colorIndex]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = (canvas.data.cols // 2) - (len(canvas.data.fallingPiece[0]) // 2)
    logging.info(f"new piece created: {canvas.data.fallingPieceColor}, position: "
                  f"({canvas.data.fallingPieceRow}, {canvas.data.fallingPieceCol})")

def drawTetrisBoard():
    logging.info("drawing the Tetris board")
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(tetrisBoard)):
        for col in range(len(tetrisBoard[0])):
            drawCell(tetrisBoard, row, col,tetrisBoard[row][col])


def drawFallingPiece():
    logging.info("drawing the falling piece")
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(canvas.data.fallingPiece)):
        for col in range(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                drawCell(tetrisBoard, row+canvas.data.fallingPieceRow, col+canvas.data.fallingPieceCol,canvas.data.fallingPieceColor)
                
def drawScore():
        cx = canvas.data.canvasWidth - 80
        cy = 20
        score = "Score: " +  str(canvas.data.score)
        canvas.create_text(cx, cy, text=score, font=("Helvetica", 12, "bold"), fill="white")    

def drawGame():
    logging.info("drawing game")
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + canvas.data.cols*cellSize
    canvasHeight = 2*margin + canvas.data.rows*cellSize
    canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="orange")
    drawTetrisBoard() 

def drawCell(board,row,col,color):
    margin = 5
    cellSize = 30
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="black")
    bordersize = 0
    canvas.create_rectangle(left+bordersize, top+bordersize, right-bordersize, bottom-bordersize, fill=color)
    logging.info(f"drew cell at Row={row}, Col={col}, Color={color}.")
    
def moveFallingPiece(drow, dcol):
    initialrow = canvas.data.fallingPieceRow
    initialcol = canvas.data.fallingPieceCol
    canvas.data.fallingPieceRow += drow
    canvas.data.fallingPieceCol += dcol
    if(fallingPieceIsLegal() == False):
        canvas.data.fallingPieceRow = initialrow
        canvas.data.fallingPieceCol = initialcol
        return False
    logging.info(f"piece moved: ({drow}, {dcol}). New position: "
                 f"({canvas.data.fallingPieceRow}, {canvas.data.fallingPieceCol})")
    return True

def placeFallingPiece():
    logging.info("placing falling piece on the board")
    for row in range(len(canvas.data.fallingPiece)):
        for col in range(len(canvas.data.fallingPiece[0])):
            if(canvas.data.fallingPiece[row][col] == True):
                canvas.data.tetrisBoard[int(row+canvas.data.fallingPieceRow)][int(col+canvas.data.fallingPieceCol)] = canvas.data.fallingPieceColor
    logging.info(f"piece placed at row {canvas.data.fallingPieceRow}")
    redrawAll()


def fallingPieceIsLegal():
    logging.debug("checking if the falling piece is in a legal position")
    tetrisBoard = canvas.data.tetrisBoard
    for row in range(len(canvas.data.fallingPiece)):
        for col in range(len(canvas.data.fallingPiece[0])):
            if canvas.data.fallingPiece[row][col]:
                absRow = row + canvas.data.fallingPieceRow
                absCol = col + canvas.data.fallingPieceCol

                if absRow >= canvas.data.rows or absRow < 0:
                    logging.warning(f"illegal position: row {absRow} is out of bounds")
                    return False
                if absCol >= canvas.data.cols or absCol < 0:
                    logging.warning(f"illegal position: col {absCol} is out of bounds")
                    return False
                if tetrisBoard[absRow][absCol] != canvas.data.emptyColor:
                    logging.warning(f"illegal position: cell [{absRow}, {absCol}] is occupied")
                    return False
    logging.debug("falling piece is in a legal position")
    return True
            
def redrawAll():
    removeFullRows()
    if (canvas.data.isGameOver == True):
        logging.info("game over state reached, displaying 'Game Over' message")
        cx = canvas.data.canvasWidth/2
        cy = canvas.data.canvasHeight/2
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
    else:
        canvas.delete(ALL)
        drawGame()
        drawFallingPiece()
        drawScore()
        logging.debug("screen redrawn successfully")

def turnCounterClockwise(piece):
    logging.info("rotating piece counterclockwise")
    sublist = []
    rotatedPiece = []
    for x in range(len(piece[0])):
        for y in range(len(piece)):
            sublist.append(piece[y][x])
        rotatedPiece.append(sublist)
        sublist = []
    rotatedPiece.reverse()
    logging.info(f"piece rotated successfully, new shape: {rotatedPiece}")
    return rotatedPiece

def rotateFallingPiece():
    logging.info("attemping to rotate falling piece")
    oldPiece = canvas.data.fallingPiece
    oldRow = canvas.data.fallingPieceRow
    oldCol = canvas.data.fallingPieceCol
    oldCollen = len(canvas.data.fallingPiece[0])
    newCol = oldRow
    newRow = (oldCollen-1) - oldCol
    (oldCenterRow, oldCenterCol) = fallingPieceCenter()
    newPiece = turnCounterClockwise(oldPiece)
    canvas.data.fallingPiece = newPiece
    canvas.data.fallingPieceRow = newRow
    canvas.data.fallingPieceCol = newCol
    (newCenterRow, newCenterCol) = fallingPieceCenter() 
    canvas.data.fallingPieceRow += oldCenterRow - newCenterRow
    canvas.data.fallingPieceCol += oldCenterCol - newCenterCol
    if(fallingPieceIsLegal()):
        logging.info(f"piece rotated successfully. New position: "
                     f"({canvas.data.fallingPieceRow}, {canvas.data.fallingPieceCol})")
        drawFallingPiece()
    else:
        logging.warning("illegal rotation attempted. Reverting to previous state")
        canvas.data.fallingPiece = oldPiece
        canvas.data.fallingPieceRow = oldRow
        canvas.data.fallingPieceCol = oldCol        

def fallingPieceCenter():
    row = canvas.data.fallingPieceRow + len(canvas.data.fallingPiece)/2
    col = canvas.data.fallingPieceCol + len(canvas.data.fallingPiece[0])/2
    logging.debug(f"falling piece center calculated: ({row}, {col})")
    return (row,col)

def removeFullRows():
    fullRows = 0
    newRow = canvas.data.rows-1
    for oldRow in range(canvas.data.rows-1, 0,-1):
        if(canvas.data.emptyColor in canvas.data.tetrisBoard[oldRow]):
            canvas.data.tetrisBoard[newRow] = copy.deepcopy(canvas.data.tetrisBoard[oldRow])
            newRow -= 1
        else:
            fullRows += 1
    for x in range(newRow-1, 0,-1):
        canvas.data.tetrisBoard[x] = [canvas.data.emptyColor]*canvas.data.cols
    canvas.data.score += (fullRows**2)*100
    logging.info(f"{fullRows} rows removed. Score updated: {canvas.data.score}")
        
def timerFired():
    logging.info("timer ticked")
    if(moveFallingPiece(1,0) == False):
        placeFallingPiece()
        newFallingPiece()
        if(fallingPieceIsLegal() == False):
            canvas.data.isGameOver = True
            logging.info("game over, no legal moves available")
    redrawAll()
    delay = 600
    canvas.after(delay, timerFired)

def keyPressed(event):
    logging.info(f"key pressed: {event.keysym}")
    if (event.char == "q"):
        canvas.data.isGameOver = True
        logging.info("game over")
    elif (event.char == "r"):
        logging.info("game restarted")
        init()    
    if (canvas.data.isGameOver == False):
        if (event.keysym == "Down"):
            moveFallingPiece(1, 0)
        elif (event.keysym == "Left"):
            moveFallingPiece(0,-1)
        elif (event.keysym == "Right"):
            moveFallingPiece(0,1)
        elif (event.keysym == "Up"):
            rotateFallingPiece()
    redrawAll()


def run(rows, cols):
    logging.info(f"starting game with board size {rows}x{cols}")
    global canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    root.canvas = canvas.canvas = canvas
    class Struct: pass
    canvas.data = Struct()
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    init()
    root.bind("<Key>", keyPressed)
    if(canvas.data.isGameOver == False):
        timerFired()
    logging.info("game loop started")
    root.mainloop()

#Run the program with the indicated size of tetris board
run(15,10)
import pygame
import math
pygame.init()

pygame.display.set_caption("Checkers")

boardSize = 600
uiSize = 120
screenSize = boardSize + uiSize

screen = pygame.display.set_mode((screenSize, screenSize))

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

RED = (255, 0, 0)

GRAY = (211, 211, 211)

DARK_GRAY = (105, 105, 105)

squareSize = boardSize // 8

blackPieceImg = pygame.image.load('./graphics/black-piece.png')
redPieceImg = pygame.image.load('./graphics/red-piece.png')
blackKingImg = pygame.image.load('./graphics/black-king.png')
redKingImg = pygame.image.load('./graphics/red-king.png')


grid = [[None] * 8 for n in range(8)]
gameInProgress = False
currentTurn = "b"
selectedChecker = [None, None]


#Initializes a new game by emptying the grid and setting the pieces
def startNewGame():
	global gameInProgress 
	global currentTurn
	global grid
	grid = [[None] * 8 for n in range(8)]
	currentTurn = "b"
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			if y < 3 and not (x + y) % 2:
				grid[y][x] = "bp"
			elif y > 4 and not (x + y) % 2:
				grid[y][x] = "rp"
	gameInProgress = True

#Draws the checkerboard pattern of the grid
def drawGrid():
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			color = RED if (x + y) % 2 else BLACK
			box = pygame.Rect(x * squareSize, y * squareSize, squareSize, squareSize)
			pygame.draw.rect(screen, color, box)
			
#Draws the pieces using the coordinates of the pieces set in grid	
def drawPieces():
	if gameInProgress:
		# if grid[4][4] != None:
		# 	print(grid)
		for y in range(len(grid)):
			for x in range(len(grid[y])):
				piece = grid[y][x]
				pieceImg = None
				if piece is not None:
					if piece == "bp":
						pieceImg = blackPieceImg
					elif piece == "rp":
						pieceImg = redPieceImg
					elif piece == "bk":
						pieceImg = blackKingImg
					elif piece == "rk":
						pieceImg = redKingImg
					pieceImgResized = pygame.transform.scale(pieceImg, (squareSize, squareSize))
					screen.blit(pieceImgResized, ((x * squareSize) - 1, (y * squareSize) - 1))
#Draws the UI 
def drawUI():
	#Draw newgame button
	btnNGWidth  = 100
	btnNGHeight = 35
	btnNGX      = (boardSize / 2) - (btnNGWidth / 2)
	btnNGY      = boardSize + ((screenSize - boardSize) / 2) - (btnNGHeight / 2)
	borderSize  = 2
	
	button(btnNGX, btnNGY, btnNGWidth, btnNGHeight, "New Game", 16, "freesansbold.ttf", BLACK, GRAY, DARK_GRAY, borderSize, startNewGame)

	#Draw current turn
	if gameInProgress:
		textSurface, textRect, = textObject("Current Turn: ", "freesansbold.ttf", 16, BLACK)
		textRect.center = ((boardSize + (screenSize - boardSize) / 2), 50)
		screen.blit(textSurface, textRect)

		colorRect = pygame.Rect((boardSize + (screenSize - boardSize) / 2) - 25, 75, 50, 50)
		color = RED if currentTurn == "r" else BLACK
		pygame.draw.rect(screen, color, colorRect)

#A utility function I made so I can make as many buttons as I want without reusing code
def button(x, y, w, h, text, textSize, textFontName, textColor, color, borderColor = None, borderSize = None, action = None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		if click[0] == 1 and action != None:
			action() 

	if borderColor and borderSize:
		border = pygame.Rect(x - borderSize, y - borderSize, w + (borderSize * 2), h + (borderSize * 2))
		pygame.draw.rect(screen, borderColor, border)
	btnRect = pygame.Rect(x, y, w, h)
	pygame.draw.rect(screen, color, btnRect)

	textSurface, textRect, = textObject(text, textFontName, textSize, textColor)
	textRect.center = btnRect.center
	screen.blit(textSurface, textRect)

#Another utility function to make a pygame text object without reusing code
def textObject(text, font, fontSize, color):
	fontRenderer = pygame.font.Font(font, fontSize)
	textSurface = fontRenderer.render(text, True, color)
	return textSurface, textSurface.get_rect()

#Handles movement of pieces
def handleMovement(event):
	global grid
	global selectedChecker
	global currentTurn
	if gameInProgress:
		#Make sure their selection is within the board
		if boardSize > pygame.mouse.get_pos()[0] > 0 and boardSize > pygame.mouse.get_pos()[1] > 0:
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				selectedChecker[0] = math.ceil(pygame.mouse.get_pos()[0] / squareSize) - 1
				selectedChecker[1] = math.ceil(pygame.mouse.get_pos()[1] / squareSize) - 1
				#If the checker is owned by the current turn
				if grid[selectedChecker[1]][selectedChecker[0]] == currentTurn + "p" or grid[selectedChecker[1]][selectedChecker[0]] == currentTurn + "k":
					#This will be used later for other stuff that is done on mousedown
					pass
				else:
					selectedChecker = [None, None]
			#If the mousebutton is being released
			if event.type == pygame.MOUSEBUTTONUP and selectedChecker != [None, None]:
				moveToX = math.ceil(pygame.mouse.get_pos()[0] / squareSize) - 1
				moveToY = math.ceil(pygame.mouse.get_pos()[1] / squareSize) - 1
				if moveToX != selectedChecker[0] and moveToY != selectedChecker[1]:
					#If the square the checker is moving to is on the black squares
					if not (moveToX + moveToY) % 2:
						validMove = False
						if grid[selectedChecker[1]][selectedChecker[0]][-1] == "p":
							#We already check using modulo if the piece is on a black square but we dont check if its on the black square in front of the piece
							if currentTurn == "r":
								if (selectedChecker[0] + 1 == moveToX or selectedChecker[0] - 1 == moveToX) and selectedChecker[1] - 1 == moveToY:
									validMove = True
							elif currentTurn == "b":
								if (selectedChecker[0] + 1 == moveToX or selectedChecker[0] - 1 == moveToX) and selectedChecker[1] + 1 == moveToY:
									validMove = True
						elif grid[selectedChecker[1]][selectedChecker[0]][-1] == "k":
							#Kings can move any distance, any diagonal direction as long as there is no piece in the way
							if moveToX > selectedChecker[0] or moveToX < selectedChecker[0]:
								if moveToY > selectedChecker[1] or moveToY < selectedChecker[1]:
									validMove = True
						if validMove:
							if currentTurn == "r" and moveToY == 0:
								grid[moveToY][moveToX] = "rk"
							elif currentTurn == "b" and moveToY == 7:
								grid[moveToY][moveToX] = "bk"
							else:
								grid[moveToY][moveToX] = grid[selectedChecker[1]][selectedChecker[0]]
							grid[selectedChecker[1]][selectedChecker[0]] = None
							currentTurn = "r" if currentTurn == "b" else "b"
				selectedChecker = [None, None]

running = True
clock = pygame.time.Clock()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
			handleMovement(event)
	screen.fill(WHITE)
	drawGrid()
	drawUI()
	drawPieces()			
	pygame.display.flip()
	clock.tick(15)
pygame.quit()
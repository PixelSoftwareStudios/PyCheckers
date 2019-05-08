import pygame
import math
import time
import json

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

bpImg = pygame.image.load('./graphics/black-piece.png')
rpImg = pygame.image.load('./graphics/red-piece.png')
bkImg = pygame.image.load('./graphics/black-king.png')
rkImg = pygame.image.load('./graphics/red-king.png')


grid = [[None] * 8 for n in range(8)]
gameInProgress = False
currentTurn = "b"
selectedChecker = [None, None]
capturedPieces = {"rp": 0, "bp": 0, "rk": 0, "bk": 0}
winner = ""

#settings will be put in JSON file and be able to be modified in game later
forcedCapture = False
flyingKings = True
forcedJumps = True
# config = json.loads(open("config.json", "r+"))

#Utility Functions:

#Draw text to the screen 
def drawTextObject(text, fontSize, color, center, font = "freesansbold.ttf"):
	fontRenderer = pygame.font.Font(font, fontSize)
	textSurface = fontRenderer.render(text, True, color)
	textRect = textSurface.get_rect()
	textRect.center = center
	screen.blit(textSurface, textRect)

def drawPieceImg(pieceType, x, y, resizeW = None, resizeH = None):
	pieceImg = None
	if pieceType is not None:
		if pieceType == "bp":
			pieceImg = bpImg
		elif pieceType == "rp":
			pieceImg = rpImg
		elif pieceType == "bk":
			pieceImg = bkImg
		elif pieceType == "rk":
			pieceImg = rkImg
		if pieceImg and resizeW and resizeH:
			pieceImg = pygame.transform.scale(pieceImg, (resizeW, resizeH))
		screen.blit(pieceImg, (x, y))

#Draws a rect to the screen that can be a simple rect or a button with an onclick action
#Required Parameters: [x, y, w, h, color, ]
#Optional Parameters: [text, textSize, textColor, font, borderSize, borderColor, action]
def rect(args):
	if "action" in args:
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if args["x"] + args["w"] > mouse[0] > args["x"] and args["y"] + args["h"] > mouse[1] > args["y"]:
			if click[0] == 1:
				args["action"]() 

	if "borderColor" in args and "borderSize" in args:
		border = pygame.Rect(args["x"] - args["borderSize"], args["y"] - args["borderSize"], args["w"] + (args["borderSize"] * 2), args["h"] + (args["borderSize"] * 2))
		pygame.draw.rect(screen, args["borderColor"], border)

	box = pygame.Rect(args["x"], args["y"], args["w"], args["h"])
	pygame.draw.rect(screen, args["color"], box)

	if "text" in args:
		if not "textSize" in args:
			args["textSize"] = 16
		if not "textColor" in args:
			args["textColor"] = BLACK
		if not "font" in args:
			args["font"] = "freesansbold.ttf"
		drawTextObject(args["text"], args["textSize"], args["textColor"], box.center, args["font"])

#Initializes a new game by emptying the grid and setting the pieces
def startNewGame():
	global gameInProgress 
	global currentTurn
	global grid
	global capturedPieces
	grid = [[None] * 8 for n in range(8)]
	currentTurn = "b"
	capturedPieces = {"rp": 0, "bp": 0, "rk": 0, "bk": 0}
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
			rect({"x": x * squareSize, "y": y * squareSize, "w": squareSize, "h": squareSize, "color": color})
			

#Draws the pieces using the coordinates of the pieces set in grid	
def drawPieces():
	if gameInProgress:
		for y in range(len(grid)):
			for x in range(len(grid[y])):
				piece = grid[y][x]
				drawPieceImg(piece, (x * squareSize) - 1, (y * squareSize) - 1, squareSize, squareSize)
#Draws the UI 
def drawUI():
	#TODO: Add save and load game buttons 
	#TODO: Add settings (flying kings, forced capture)
	#TODO: Add forfeit button
	#Draw newgame button
	btnNGWidth  = 100
	btnNGHeight = 35
	btnNGX      = (boardSize / 2) - (btnNGWidth / 2)
	btnNGY      = boardSize + ((screenSize - boardSize) / 2) - (btnNGHeight / 2)
	rect({"x": btnNGX, "y": btnNGY, "w": btnNGWidth, "h": btnNGHeight, "color": GRAY, "text": "New Game", "borderSize": 2, "borderColor": BLACK, "action": startNewGame})
	#All UI other than New Game button should be displayed after game starts
	if gameInProgress:
	#Draw current turn
		drawTextObject("Current Turn: ", 16, BLACK, ((boardSize + (screenSize - boardSize) / 2), 50))
		colorRectX = (boardSize + (screenSize - boardSize) / 2) - 25
		colorRectY = 75
		color = RED if currentTurn == "r" else BLACK
		rect({"x": colorRectX, "y": colorRectY, "w": 50, "h": 50, "color": color})
	#Draw captured piece box
		drawTextObject("Captured ", 16, BLACK, ((boardSize + (screenSize - boardSize) / 2), 150))
		drawTextObject("Pieces: ", 16, BLACK, ((boardSize + (screenSize - boardSize) / 2), 170))
		capturedBoxX = (boardSize + (screenSize - boardSize) / 2) - 43
		rect({"x": capturedBoxX, "y": 202, "w": 86, "h": 396, "color": GRAY, "borderSize": 2, "borderColor": DARK_GRAY})
	
	#Draw captured pieces
		capturedPiecesX = (boardSize + (screenSize - boardSize) / 2)
		for pieceType, pieceCount in capturedPieces.items():
			if pieceCount > 0:
				pieceY = 200 if pieceType == "rp" else 510 
				drawPieceImg(pieceType, capturedPiecesX - 35, pieceY, 70, 70)
			if pieceCount > 1: 
				textY = 285 if pieceType == "rp" else 590
				drawTextObject("x" + str(pieceCount), 16, BLACK, (capturedPiecesX, textY))
#Handles movement of pieces
def handleMovement(event):
	global grid
	global selectedChecker
	global currentTurn
	global capturedPieces
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
				#If it wasn't dropped on the same spot
				if moveToX != selectedChecker[0] and moveToY != selectedChecker[1]:
					#If the square the checker is moving to is on the black squares
					if not (moveToX + moveToY) % 2:
						validMove = False
						xOffset = 0
						yOffset = 0
						#If the piece is not trying to capture one of its own
						if grid[moveToY][moveToX] != currentTurn + "p" and grid[moveToY][moveToX] != currentTurn + "k":
							#If the selected piece is a normal piece
							if grid[selectedChecker[1]][selectedChecker[0]][-1] == "p":
								#If there is no piece at the square the checker is moving to
								#Or if forcedJumps is disabled it doesnt matter if there is a piece
								if grid[moveToY][moveToX] == None or not forcedJumps:
									#Depending on the current turn it checks if the checker is moving to
									# The two diagonal spots in front of it	
									if currentTurn == "r":
										if (selectedChecker[0] + 1 == moveToX or selectedChecker[0] - 1 == moveToX) and selectedChecker[1] - 1 == moveToY:
											validMove = True
									elif currentTurn == "b":
										if (selectedChecker[0] + 1 == moveToX or selectedChecker[0] - 1 == moveToX) and selectedChecker[1] + 1 == moveToY:
											validMove = True
								#If there is a piece at the spot the checker is trying to move to and the checker has to jump
								if forcedJumps and grid[moveToY][moveToX]:
									#Determine the X and Y offset which is the direction the spot is to the position of the checker
									if moveToX > selectedChecker[0]:
										xOffset = 1
									if moveToX < selectedChecker[0]:
										xOffset = -1 
									if moveToY > selectedChecker[1]:
										yOffset = 1
									if moveToY < selectedChecker[1]:
										yOffset = -1
									#If the spot after the spot the checker is moving to is on the board
									if 7 > moveToX + xOffset > 0 and 7 > moveToY + yOffset > 0:
										#If the spot after the spot the checker is moving to is empty
										if not grid[moveToY + yOffset][moveToX + xOffset]:
											moveToY = moveToY + yOffset
											moveToX = moveToX + xOffset
											validMove = True
									else:
										#If the spot is off the board then 
										#its ok to capture the piece even if its not technically jumping
										validMove = True
							#If the piece is a king
							elif grid[selectedChecker[1]][selectedChecker[0]][-1] == "k":
								#If the settings allow kings to go any distance instead of just 1 square
								if flyingKings:
									xOffset = 0
									yOffset = 0
									if moveToX > selectedChecker[0]:
										xOffset = 1
									if moveToX < selectedChecker[0]:
										xOffset = -1 
									if moveToY > selectedChecker[1]:
										yOffset = 1
									if moveToY < selectedChecker[1]:
										yOffset = -1 
									#If the king is moving on a diagonal
									if xOffset != 0 and yOffset != 0:
										#Check if there is a piece in the way
										x = selectedChecker[0] + xOffset
										for y in range(selectedChecker[1] + yOffset, moveToY):
											if grid[y][x] != None:
												break
											x += xOffset
								else:
									if (selectedChecker[0] + 1 == moveToX or selectedChecker[0] - 1 == moveToX) and (selectedChecker[1] - 1 == moveToY or selectedChecker[1] + 1 == moveToY):
										validMove = True
						if validMove:
							#If there is an opponent piece in the spot the selected piece is moving to, and forcedJumps = False
							#Or if the spot to the left/right of the opponent piece is within boundaries and forcedJumps
							if grid[moveToY][moveToX] and (not forcedJumps or ((7 > moveToX + xOffset > 0 and 7 > moveToY + yOffset > 0) and forcedJumps)):
								capturedPieces[grid[moveToY][moveToX]] += 1
								grid[moveToY][moveToX] = None
							elif not grid[moveToY][moveToX] and grid[selectedChecker[1]][selectedChecker[0]][-1] == "p" and grid[moveToY - yOffset][moveToX - xOffset]:
								capturedPieces[grid[moveToY - yOffset][moveToX - xOffset]] += 1
								grid[moveToY - yOffset][moveToX - xOffset] = None
							if currentTurn == "r" and moveToY == 0:
								grid[moveToY][moveToX] = "rk"
							elif currentTurn == "b" and moveToY == 7:
								grid[moveToY][moveToX] = "bk"
							else:
								grid[moveToY][moveToX] = grid[selectedChecker[1]][selectedChecker[0]]
							grid[selectedChecker[1]][selectedChecker[0]] = None
							currentTurn = "r" if currentTurn == "b" else "b"
				selectedChecker = [None, None]
			
			# if event.type == pygame.MOUSEMOTION and selectedChecker != [None, None]:
			# 	print(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
			# 	drawPieceImg(grid[selectedChecker[1]][selectedChecker[0]], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], squareSize, squareSize)

running = True
clock = pygame.time.Clock()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP: #or pygame.MOUSEMOTION:
			handleMovement(event)
	screen.fill(WHITE)
	drawGrid()
	drawPieces()
	drawUI()
	pygame.display.flip()
	clock.tick(15)
pygame.quit()
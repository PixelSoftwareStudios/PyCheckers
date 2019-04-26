import pygame
import math
pygame.init()

pygame.display.set_caption("Checkers")

screendim = 720
boardSize = 600

screen = pygame.display.set_mode((screendim, screendim))

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

RED = (255, 0, 0)

squareSize = boardSize // 8

blackPieceImg = pygame.image.load('./graphics/black-piece.png')
redPieceImg = pygame.image.load('./graphics/red-piece.png')
blackKingImg = pygame.image.load('./graphics/black-king.png')
redKingImg = pygame.image.load('./graphics/red-piece.png')

grid = [[n]*8 for n in range(8)]
piecesList = [
	[0, 0, "bp"], [2, 0, "bp"], [4, 0, "bp"], [6, 0, "bp"], 
	[1, 1, "bp"], [3, 1, "bp"], [5, 1, "bp"], [7, 1, "bp"],
	[0, 2, "bp"], [2, 2, "bp"], [4, 2, "bp"], [6, 2, "bp"],
	[1, 5, "rp"], [3, 5, "rp"], [5, 5, "rp"], [7, 5, "rp"],
	[0, 6, "rp"], [2, 6, "rp"], [4, 6, "rp"], [6, 6, "rp"],
	[1, 7, "rp"], [3, 7, "rp"], [5, 7, "rp"], [7, 7, "rp"]
]
# def drawGrid():
# 	x = 0
# 	y = 0
# 	#J is where in the row the first red square is
# 	j = 0
# 	for row in grid:
# 		i = j
# 		while (i < len(row)):
# 			row[i] = "r"
# 			if (i + 2 <= len(row)):
# 				i += 2
# 		for col in row:
# 			color = BLACK
# 			if x - w 
# 			if col == "r":
# 				color = RED
# 			box = pygame.Rect(x, y, w, w)
# 			pygame.draw.rect(screen, color, box)

# 			x = x + w
# 		y = y + w
# 		x = 0
# 		j += 1
def drawGrid():
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			color = RED if (x + y) % 2 else BLACK
			box = pygame.Rect(x * squareSize, y * squareSize, squareSize, squareSize)
			pygame.draw.rect(screen, color, box)
def drawPieces():
	for piece in piecesList:
		if piece[2] == "bp":
			pieceImg = blackPieceImg
		elif piece[2] == "rp":
			pieceImg = redPieceImg
		elif piece[2] == "bk":
			pieceImg = blackKingImg
		elif piece[2] == "rk":
			pieceImg = redKingImg
		pieceImgResized = pygame.transform.scale(pieceImg, (squareSize, squareSize))
		screen.blit(pieceImgResized, ((piece[0] * squareSize) - 1, (piece[1] * squareSize) - 1))
def drawUI():
	pass
moveTo = [None, None]
selectedChecker = [None, None]
def checkForMovement():
	moveTo = [None, None]
	selectedChecker = [None, None]
	firstMouseDown = True
	if pygame.mouse.get_pressed()[0]:
		if firstMouseDown:
			selectedChecker[0] = math.ceil(pygame.mouse.get_pos()[0] / squareSize) - 1
			selectedChecker[1] = math.ceil(pygame.mouse.get_pos()[1] / squareSize) - 1
			print(selectedChecker)
			firstMouseDown = False
		moveTo[0] = math.ceil(pygame.mouse.get_pos()[0] / squareSize) - 1
		moveTo[1] = math.ceil(pygame.mouse.get_pos()[1] / squareSize) - 1
		print(moveTo)
	if moveTo is not [None, None]:
		if selectedChecker is not [None, None]:
			if moveTo[0] is not selectedChecker[0] and moveTo[1] is not selectedChecker[1]:
				print("b")
				for piece in piecesList:
					if piece[0] == selectedChecker[0] and piece[1] == selectedChecker[1]:
						print("o")
						piece[0] = moveTo[0]
						piece[1] = moveTo[1]

			# if (piece[0] == onGridCoords[0] and piece[1] == onGridCoords[1]):
			
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
	screen.fill(WHITE)
	drawGrid()
	drawPieces()
	checkForMovement()
	pygame.display.flip()
pygame.quit()

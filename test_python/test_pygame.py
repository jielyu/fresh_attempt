import pygame, sys, random
from pygame.locals import *
# 一些常量
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
BACKGROUNDCOLOR = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 40
VHNUMS = 3
CELLNUMS = VHNUMS*VHNUMS
MAXRANDTIME = 100
# 退出
def terminate():
  pygame.quit()
  sys.exit()
# 随机生成游戏盘面
def newGameBoard():
  board = []
  for i in range(CELLNUMS):
    board.append(i)
  blackCell = CELLNUMS-1
  board[blackCell] = -1
  for i in range(MAXRANDTIME):
    direction = random.randint(0, 3)
    if (direction == 0):
      blackCell = moveLeft(board, blackCell)
    elif (direction == 1):
      blackCell = moveRight(board, blackCell)
    elif (direction == 2):
      blackCell = moveUp(board, blackCell)
    elif (direction == 3):
      blackCell = moveDown(board, blackCell)
  return board, blackCell
# 若空白图像块不在最左边，则将空白块左边的块移动到空白块位置 
def moveRight(board, blackCell):
  if blackCell % VHNUMS == 0:
    return blackCell
  board[blackCell-1], board[blackCell] = board[blackCell], board[blackCell-1]
  return blackCell-1
# 若空白图像块不在最右边，则将空白块右边的块移动到空白块位置 
def moveLeft(board, blackCell):
  if blackCell % VHNUMS == VHNUMS-1:
    return blackCell
  board[blackCell+1], board[blackCell] = board[blackCell], board[blackCell+1]
  return blackCell+1
# 若空白图像块不在最上边，则将空白块上边的块移动到空白块位置 
def moveDown(board, blackCell):
  if blackCell < VHNUMS:
    return blackCell
  board[blackCell-VHNUMS], board[blackCell] = board[blackCell], board[blackCell-VHNUMS]
  return blackCell-VHNUMS
# 若空白图像块不在最下边，则将空白块下边的块移动到空白块位置 
def moveUp(board, blackCell):
  if blackCell >= CELLNUMS-VHNUMS:
    return blackCell
  board[blackCell+VHNUMS], board[blackCell] = board[blackCell], board[blackCell+VHNUMS]
  return blackCell+VHNUMS
# 是否完成
def isFinished(board, blackCell):
  for i in range(CELLNUMS-1):
    if board[i] != i:
      return False
  return True
# 初始化
pygame.init()
mainClock = pygame.time.Clock()
# 加载图片
gameImage = pygame.image.load('001.png')
gameRect = gameImage.get_rect()
# 设置窗口
windowSurface = pygame.display.set_mode((gameRect.width, gameRect.height))
pygame.display.set_caption('拼图')
cellWidth = int(gameRect.width / VHNUMS)
cellHeight = int(gameRect.height / VHNUMS)
finish = False
gameBoard, blackCell = newGameBoard()
# 游戏主循环
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      terminate()
    if finish:
      continue
    if event.type == KEYDOWN:
      if event.key == K_LEFT or event.key == ord('a'):
        blackCell = moveLeft(gameBoard, blackCell)
      if event.key == K_RIGHT or event.key == ord('d'):
        blackCell = moveRight(gameBoard, blackCell)
      if event.key == K_UP or event.key == ord('w'):
        blackCell = moveUp(gameBoard, blackCell)
      if event.key == K_DOWN or event.key == ord('s'):
        blackCell = moveDown(gameBoard, blackCell)
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
      x, y = pygame.mouse.get_pos()
      col = int(x / cellWidth)
      row = int(y / cellHeight)
      index = col + row*VHNUMS
      if (index == blackCell-1 or index == blackCell+1 or index == blackCell-VHNUMS or index == blackCell+VHNUMS):
        gameBoard[blackCell], gameBoard[index] = gameBoard[index], gameBoard[blackCell]
        blackCell = index
  if (isFinished(gameBoard, blackCell)):
    gameBoard[blackCell] = CELLNUMS-1
    finish = True
  windowSurface.fill(BACKGROUNDCOLOR)
  for i in range(CELLNUMS):
    rowDst = int(i / VHNUMS)
    colDst = int(i % VHNUMS)
    rectDst = pygame.Rect(colDst*cellWidth, rowDst*cellHeight, cellWidth, cellHeight)
    if gameBoard[i] == -1:
      continue
    rowArea = int(gameBoard[i] / VHNUMS)
    colArea = int(gameBoard[i] % VHNUMS)
    rectArea = pygame.Rect(colArea*cellWidth, rowArea*cellHeight, cellWidth, cellHeight)
    windowSurface.blit(gameImage, rectDst, rectArea)
  for i in range(VHNUMS+1):
    pygame.draw.line(windowSurface, BLACK, (i*cellWidth, 0), (i*cellWidth, gameRect.height))
  for i in range(VHNUMS+1):
    pygame.draw.line(windowSurface, BLACK, (0, i*cellHeight), (gameRect.width, i*cellHeight))
  pygame.display.update()
  mainClock.tick(FPS)
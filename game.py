import curses
import random
import time

COLOR_GREEN = 1

RECT_WIDTH = 3
RECT_HEIGHT = 2
NUM_CARS_IN_ROW = 4
CAR_WIDTH = RECT_WIDTH * 3
CAR_HEIGHT = RECT_HEIGHT * 4
SPEED = 1
CAR_POSITIONS = [(0, 2), (0, 3), (1, 3), 0, 1, 2, 3]

class Game():
  def __init__(self, screen):
    self.screen = screen
    self.cars = []
    self.player = Car(CAR_WIDTH, curses.LINES - CAR_HEIGHT - 1)
    self.done = False

    curses.start_color()
    curses.init_pair(COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)

  def update(self, action, render=False, speed=0.01):
    if self.screen and render:
      self.screen.clear()
      self.drawPlayer()
    self.cars = list(filter(lambda car: car.y < curses.LINES, self.cars))
    if len(self.cars) == 0 or min(self.cars, key=lambda car: car.y).y >= CAR_HEIGHT + 3:
      self.generateRow()
    for car in self.cars:
      car.update()
      if self.screen and render:
        car.draw(self.screen)
    if action == 0:
      self.player.x = max(0, self.player.x - CAR_WIDTH)
    elif action == 2:
      self.player.x = min((NUM_CARS_IN_ROW - 1) * CAR_WIDTH, self.player.x + CAR_WIDTH)

    self.checkCollision()

    if self.screen and render:
      self.screen.refresh()
      time.sleep(speed)

    if len(self.cars) < 3:
      return None

    sorted_cars = sorted(self.cars, key=lambda car: car.y, reverse=True)
    reward = -2 if self.done else 1
    if action == 1 and not self.done:
      reward = 3

    return ((sorted_cars[0].xPosition(), sorted_cars[0].y, sorted_cars[1].xPosition(), sorted_cars[1].y, sorted_cars[2].xPosition(), sorted_cars[2].y, self.player.xPosition()), reward)

  def generateRow(self):
    position = random.choice(CAR_POSITIONS)
    if isinstance(position, int):
      self.cars.append(Car(position * CAR_WIDTH, -CAR_HEIGHT))
    elif isinstance(position, list):
      for value in position:
        self.cars.append(Car(value * CAR_WIDTH, -CAR_HEIGHT))

  def drawPlayer(self, ch=178):
    self.player.draw(self.screen, ch, color=COLOR_GREEN)

  def checkCollision(self):
    for car in self.cars:
      if car.y < curses.LINES - 2 * CAR_HEIGHT + 1 or car.y >= curses.LINES - 2:
        continue
      elif car.x == self.player.x:
        self.done = True

class Car():
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def update(self):
    self.y += 1

  def draw(self, screen, ch=178, color=None):
    c = chr(ch)
    tuples = [
      (self.x + RECT_WIDTH, self.y), 
      (self.x, self.y + RECT_HEIGHT),
      (self.x + 2 * RECT_WIDTH, self.y + RECT_HEIGHT),
      (self.x + RECT_WIDTH, self.y + RECT_HEIGHT * 2),
      (self.x, self.y + RECT_HEIGHT * 3),
      (self.x + 2 * RECT_WIDTH, self.y + RECT_HEIGHT * 3)
    ]
    for t in tuples:
      self.drawRect(screen, RECT_WIDTH, RECT_HEIGHT, t[0], t[1], c, color)
      
  def drawRect(self, screen, width, height, x, y, chr, color=None):
    line = "".join([chr * width])
    for l in range(y, y + height):
      if l < 0:
        continue
      elif l >= curses.LINES:
        return
      screen.addstr(l, x, line, curses.color_pair(COLOR_GREEN) if color else 0)

  def xPosition(self):
    return self.x // CAR_WIDTH
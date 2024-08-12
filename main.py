import pygame
import random

pygame.init()

win = pygame.display.set_mode((750, 750))

pygame.display.set_caption('Space Invaders')

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

class Ship(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([50, 25])
    self.image.fill(green)
    self.rect = self.image.get_rect()
    self.lives = 5

  def draw(self):
    win.blit(self.image, (self.rect.x, self.rect.y))
  
class Enemy(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([25, 25])
    self.image.fill(white)
    self.rect = self.image.get_rect()

class Bunker(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([8,8])
    self.image.fill(green)
    self.rect = self.image.get_rect()

class Missile(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([5, 10])
    self.image.fill(green)
    self.rect = self.image.get_rect()

  def update(self):
    self.rect.y += -10

class Bomb(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface([5, 10])
    self.image.fill(red)
    self.rect = self.image.get_rect()

  def update(self):
    self.rect.y += 10

ship = Ship()
ship.rect.x = 375
ship.rect.y = 650

enemy_list = pygame.sprite.Group()
bunker_list = pygame.sprite.Group()
missile_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()

for row in range(1, 6):
  for column in range(1, 11):
    enemy = Enemy()
    enemy.rect.x = 80 + (50 * column)
    enemy.rect.y = 25 + (50 * row)
    enemy_list.add(enemy)

for  bunk in range(3):
  for row in range(5):
    for column in range(10):
      bunker = Bunker()
      bunker.rect.x = (50 + (275 * bunk)) + (10 * column)
      bunker.rect.y = 500 + (10 * row)
      bunker_list.add(bunker)

def redraw():
  win.fill(black)
  ship.draw()
  enemy_list.draw(win)
  bunker_list.draw(win)
  missile_list.update()
  missile_list.draw(win)
  bomb_list.update()
  bomb_list.draw(win)
  pygame.display.update()

run = True

while run:
  pygame.time.delay(100)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  key = pygame.key.get_pressed()
  if key[pygame.K_LEFT]:
    ship.rect.x += -10

  if key[pygame.K_RIGHT]:
    ship.rect.x += 10

  if key[pygame.K_SPACE]:
    if len(missile_list) < 10:
      missile = Missile()
      missile.rect.x = ship.rect.x + 25
      missile.rect.y = ship.rect.y
      missile_list.add(missile)
  
  shoot_chance = random.randint(1, 100)
  if shoot_chance < 25:
    if len(enemy_list) > 0:
      random_enemy = random.choice(enemy_list.sprites())
      bomb = Bomb()
      bomb.rect.x = random_enemy.rect.x + 12
      bomb.rect.y = random_enemy.rect.y + 25
      bomb_list.add(bomb)
  
  for missile in missile_list:
    if missile.rect.y < -10:
      missile_list.remove(missile)
    for enemy in enemy_list:
      if missile.rect.colliderect(enemy.rect):
        missile_list.remove(missile)
        enemy_list.remove(enemy)

    for bunker in bunker_list:
      if missile.rect.colliderect(bunker.rect):
        missile_list.remove(missile)
        bunker_list.remove(bunker)

    for bomb in bomb_list:
      if bomb.rect.colliderect(ship.rect):
        bomb_list.remove(bomb)
        ship.lives -+ 1
      for bunker in bunker_list:
        if bomb.rect.colliderect(bunker.rect):
          bunker_list.remove(bomb)
          bunker_list.remove(bunker)
  redraw()

pygame.quit()
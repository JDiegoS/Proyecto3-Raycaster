#Juan Diego Solorzano 18151
#Proyecto 3: Raycaster
import pygame
from math import pi, cos, sin, atan2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 0, 0)

wall1 = pygame.image.load('./images/fence.png')
wall2 = pygame.image.load('./images/grass.png')
wall3 = pygame.image.load('./images/barrel.png')
wall4 = pygame.image.load('./images/oil.png')
wall5 = pygame.image.load('./images/car.png')

gun = pygame.image.load('./images/gun1.png')

textures = {
  "1": wall1,
  "2": wall2,
  "3": wall3,
  "4": wall4,
  "5": wall5
}

enemies = [
  {
    "x": 120,
    "y": 355,
    "texture": pygame.image.load('./images/alien4.png')
  },
  {
    "x": 150,
    "y": 120,
    "texture": pygame.image.load('./images/alien5.png')
  },
  {
    "x": 420,
    "y": 160,
    "texture": pygame.image.load('./images/predator.png')
  }
 
]

class Raycaster(object):
  def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect()
        self.screen = screen
        self.blocksize = 50
        self.player = {
        "x": self.blocksize + 20,
        "y": self.blocksize + 20,
        "a": 0,
        "fov": pi/3
        }
        self.map = []
        self.zbuffer = [-float('inf') for z in range(0, 500)]

  def point(self, x, y, c = None):
        screen.set_at((x, y), c)

  def draw_rectangle(self, x, y, texture):
        for cx in range(x, x + self.blocksize):
            for cy in range(y, y + self.blocksize):
                #Texture size
                tx = int((cx - x)*128 / self.blocksize)
                ty = int((cy - y)*128 / self.blocksize)
                #Textura del bloque
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c)

  def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

  def cast_ray(self, a):
        d = 0
        while True:
            x = self.player["x"] + d*cos(a)
            y = self.player["y"] + d*sin(a)

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i*50
                hity = y - j*50

                if 1 < hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity
                tx = int(maxhit * 128 / 50)

                return d, self.map[j][i], tx

            self.point(int(x), int(y), WHITE)
            d += 1

  def draw_stake(self, x, h, texture, tx):
        start = int(250 - h/2)
        end = int(250 + h/2)
        for y in range(start, end):
            #Texture
            ty = int(((y - start)*128)/(end - start))
            c = texture.get_at((tx, ty))
            if c != (0, 0, 0, 0) and c != (255, 0, 255, 255) and c != (163, 73, 164, 255):
                self.point(x, y, c)
            #print(c)
        

  def draw_sprite(self, sprite):
        sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])

        sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
        #Ancho
        sprite_size = (500/sprite_d) * 70

        #Donde esta
        sprite_x = 500 + (sprite_a - self.player["a"])*500/self.player["fov"] + 250 - sprite_size/2
        sprite_y = 250 - sprite_size/2

        sprite_x = int(sprite_x)
        sprite_y = int(sprite_y)
        sprite_size = int(sprite_size)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 500 < x < 1000 and self.zbuffer[x - 500] >= sprite_d:
                    tx = int((x - sprite_x) * 128/sprite_size)
                    ty = int((y - sprite_y) * 128/sprite_size)
                    c = sprite["texture"].get_at((tx, ty))
                    #Transparencia
                    if c != (248, 0, 248) and c != (0, 0, 0, 0) and c != (163, 73, 164, 255):
                            self.point(x, y, c)
                            self.zbuffer[x - 500] = sprite_d
                            #print(c)

  def draw_player(self, xi, yi, w = 128, h = 128):
        #Jugador first person
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 128/w)
                ty = int((y - yi) * 128/h)
                c = gun.get_at((tx, ty))
                if c != (0, 0, 0, 0):
                    self.point(x, y, c)

  def render(self):
        for x in range(0, 500, 50):
            for y in range(0, 500, 50):
                i = int(x/50)
                j = int(y/50)
                if self.map[j][i] != ' ':
                    self.draw_rectangle(x, y, textures[self.map[j][i]])

        self.point(self.player["x"], self.player["y"], (255, 255, 255))

        for i in range(0, 500):
            a =  self.player["a"] - self.player["fov"]/2 + self.player["fov"]*i/500
            d, c, tx = self.cast_ray(a)
            x = 500 + i
            #Que tan espacioso
            h = 500/(d*cos(a-self.player["a"])) * 40
            self.draw_stake(x, h, textures[c], tx)
            self.zbuffer[i] = d

        for enemy in enemies:
            self.point(enemy["x"], enemy["y"], BLACK)
            self.draw_sprite(enemy)

        self.draw_player(776, 380)

pygame.init()
screen = pygame.display.set_mode((1000, 500), pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN|pygame.HWSURFACE)
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('./map.txt')

while True:
    screen.fill((113, 113, 113))
    r.render()

    for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                exit(0)
            if e.type == pygame.KEYDOWN:
                #Movimiento wasd
                if e.key == pygame.K_a:
                    r.player["a"] -= pi/10
                elif e.key == pygame.K_d:
                    r.player["a"] += pi/10
                elif e.key == pygame.K_w:
                    r.player["x"] += int(10 * cos(r.player["a"]))
                    r.player["y"] += int(10 * sin(r.player["a"]))
                elif e.key == pygame.K_s:
                    r.player["x"] -= int(10 * cos(r.player["a"]))
                    r.player["y"] -= int(10 * sin(r.player["a"]))

    pygame.display.update()
#Juan Diego Solorzano 18151
#Proyecto 3: Raycaster
import pygame
from math import pi, cos, sin, atan2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 0, 0)

#Sprites
wall1 = pygame.image.load('./images/fence.png')
wall2 = pygame.image.load('./images/grass.png')
wall3 = pygame.image.load('./images/barrel.png')
wall4 = pygame.image.load('./images/oil.png')
wall5 = pygame.image.load('./images/car.png')

gun = pygame.image.load('./images/gun1.png')
rambo = pygame.image.load('./images/rambo.png')
hud = pygame.image.load('./images/hud.png')

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
    "y": 315,
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
        self.zbuffer = [-float('inf') for z in range(0, 1000)]
        self.close = False

  def point(self, x, y, c = None):
        screen.set_at((x, y), c)

  def draw_rectangle(self, x, y, texture):
        for cx in range(x, x + 20):
            for cy in range(y, y + 20):
                #Texture size
                tx = int((cx - x)*128 / 20)
                ty = int((cy - y)*128 / 20)
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

            i = int(x/50)
            j = int(y/50)

            if self.map[j][i] != ' ':
                hitx = x - i*50
                hity = y - j*50

                if 1 < hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity
                tx = int(maxhit * 2.56)

                return d, self.map[j][i], tx

            #self.point(int(x), int(y), WHITE)
            d += 1

  def draw_stake(self, x, h, texture, tx):
        start = int(250 - h/2)
        end = int(250 + h/2)
        for y in range(start, end):
            #Texture
            ty = int(((y - start)*128)/(end - start))
            c = texture.get_at((tx, ty))
            if c != (0, 0, 0, 0) and c != (255, 0, 255, 255):
                self.point(x, y, c)
            #print(c)
        

  def draw_sprite(self, sprite):
        sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])

        sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**0.5
        
        #Si choca
        if sprite_d <= 35:
            self.close = True
            
        #Ancho
        sprite_size = int((1000/sprite_d) * 50)

        #Donde esta
        sprite_x = int((sprite_a - self.player["a"])*1000/self.player["fov"] + 500 - sprite_size/2)
        sprite_y = int(250 - sprite_size/2)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 0 < x < 1000 and self.zbuffer[x] >= sprite_d:
                    tx = int((x - sprite_x) * 128/sprite_size)
                    ty = int((y - sprite_y) * 128/sprite_size)
                    c = sprite["texture"].get_at((tx, ty))
                    #Transparencia
                    if c != (248, 0, 248) and c != (0, 0, 0, 0) and c != (163, 73, 164, 255):
                            self.point(x, y, c)
                            self.zbuffer[x] = sprite_d
                            #print(c)

  def draw_player(self, xi, yi, w = 260, h = 280):
        #Jugador first person
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 260/w)
                ty = int((y - yi) * 280/h)
                c = gun.get_at((tx, ty))
                if c != (0, 0, 0, 0):
                    self.point(x, y, c)

  def draw_hud(self, xi, yi, w = 240, h = 80):
        #Jugador first person
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 240/w)
                ty = int((y - yi) * 80/h)
                #print(ty)
                c = hud.get_at((tx, ty))
                self.point(x, y, c)

  def draw_rambo(self, xi, yi, w = 120, h = 120):
        #Jugador first person
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * 120/w)
                ty = int((y - yi) * 120/h)
                c = rambo.get_at((tx, ty))
                self.point(x, y, c)
    
  #Referencia: https://pythonprogramming.net/pygame-start-menu-tutorial/
  def text_objects(self, text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

  def game_intro(self):
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        intro = False
                        self.game_loop()

            screen.fill(BLACK)
            largeText = pygame.font.Font('freesansbold.ttf', 55)
            TextSurf, TextRect = self.text_objects(
                "PROYECTO 2: RAYCASTER", largeText)
            TextRect.center = (500, 100)
            screen.blit(TextSurf, TextRect)

            mediumText = pygame.font.Font('freesansbold.ttf', 25)
            TextSurf, TextRect = self.text_objects(
                "You have been surrounded by aliens and predators in the jungle", mediumText)
            TextRect.center = (500, 250)
            screen.blit(TextSurf, TextRect)

            mediumText2 = pygame.font.Font('freesansbold.ttf', 25)
            TextSurf, TextRect = self.text_objects(
                "Get to the car to escape!", mediumText2)
            TextRect.center = (500, 300)
            screen.blit(TextSurf, TextRect)

            smallText = pygame.font.Font('freesansbold.ttf', 20)
            TextSurf, TextRect = self.text_objects(
                "PRESS ENTER TO START", smallText)
            TextRect.center = (500, 450)
            screen.blit(TextSurf, TextRect)
            pygame.display.update()

  def game_loop(self):
        playing = True
        #Musica
        pygame.mixer.init()
        pygame.mixer.music.load('./Sounds/song.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
        while playing:
            
            if r.player["x"] >= 300 and r.player["y"] >= 400:
                playing = False
                self.game_won()

            screen.fill((20, 20, 20))
            r.render()

            for e in pygame.event.get():
                    if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                        exit(0)
                    if e.type == pygame.KEYDOWN:
                        #Movimiento wasd
                        #No permite atravesar paredes solo moverse a los lados y atras
                        if r.close == False:
                            
                            if e.key == pygame.K_w:
                                r.player["x"] += int(15 * cos(r.player["a"]))
                                r.player["y"] += int(15 * sin(r.player["a"]))
                        
                        if e.key == pygame.K_a:
                            r.player["a"] -= pi/15
                        elif e.key == pygame.K_d:
                            r.player["a"] += pi/15
                        elif e.key == pygame.K_s:
                            r.player["x"] -= int(15 * cos(r.player["a"]))
                            r.player["y"] -= int(15 * sin(r.player["a"]))
                        r.close = False

            self.fps()
            clock.tick(60)
            pygame.display.update()

  def game_won(self):
        won = True

        #Sound effect
        pygame.mixer.music.load('./Sounds/car.mp3')
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(0.6)

        while won:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)

            screen.fill(BLACK)
            largeText = pygame.font.Font('freesansbold.ttf', 55)
            TextSurf, TextRect = self.text_objects(
                "VICTORY!", largeText)
            TextRect.center = (500, 100)
            screen.blit(TextSurf, TextRect)

            mediumText = pygame.font.Font('freesansbold.ttf', 25)
            TextSurf, TextRect = self.text_objects(
                "Thanks for playing!", mediumText)
            TextRect.center = (500, 250)
            screen.blit(TextSurf, TextRect)

            smallText = pygame.font.Font('freesansbold.ttf', 20)
            TextSurf, TextRect = self.text_objects(
                "PRESS ESCAPE TO QUIT", smallText)
            TextRect.center = (500, 450)
            screen.blit(TextSurf, TextRect)
            pygame.display.update()

  def fps(self):
        smallText = pygame.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = self.text_objects(
            "FPS: " + str(int(clock.get_fps())), smallText)
        TextRect.center = (260, 30)
        screen.blit(TextSurf, TextRect)

  def render(self):
        for i in range(0, 1000):
            a =  self.player["a"] - self.player["fov"]/2 + self.player["fov"]*i/1000
            d, c, tx = self.cast_ray(a)

            #Si choca
            if d <= 11:
                self.close = True
                continue
            x = i
            #Que tan espacioso
            h = 800/(d*cos(a-self.player["a"])) * 30
            self.draw_stake(x, h, textures[c], tx)
            self.zbuffer[i] = d

        for enemy in enemies:
            self.point(enemy["x"], enemy["y"], BLACK)
            self.draw_sprite(enemy)

        for x in range(0, 200, 20):
            for y in range(0, 200, 20):
                i = int(x/20)
                j = int(y/20)
                if self.map[j][i] != ' ':
                    self.draw_rectangle(x, y, textures[self.map[j][i]])

        self.point(int(self.player["x"]*0.4), int(self.player["y"]*0.4), (255, 255, 255))
        
        self.draw_player(576, 250)
        self.draw_rambo(880, 0)
        self.draw_hud(640, 0)

pygame.init()
screen = pygame.display.set_mode((1000, 500), pygame.DOUBLEBUF|pygame.HWACCEL|pygame.HWSURFACE)
screen.set_alpha(None)
clock = pygame.time.Clock()
r = Raycaster(screen)
r.load_map('./map.txt')
r.game_intro()


import pygame
import sys
'''меняю на свой 2'''


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, sprite):
        sprite.rect.x -= self.dx
        sprite.rect.y -= self.dy

    def update(self, sprite):
        x, y = sprite.rect.x, sprite.rect.y
        w, h = sprite.rect.width, sprite.rect.height
        self.dx = x - width // 2 + w // 2
        self.dy = y - height // 2 + h // 2


def ending():
    pygame.quit()
    sys.exit()


def intro():
    intro_screen = pygame.image.load('data/pixel_mando (2).jpg')
    intro_screen = pygame.transform.scale(intro_screen, (width, height))
    screen.blit(intro_screen, (0, 0))
    font = pygame.font.Font(None, 100)
    game_text = font.render('Play!', False, "black")
    exit_text = font.render('Exit', False, "black")
    screen.blit(game_text, (170, 400))
    screen.blit(exit_text, (1000, 400))
    game_text_rect = game_text.get_rect()
    game_text_rect.x = 170
    game_text_rect.y = 400
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.x = 1000
    exit_text_rect.y = 400

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ending()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_text_rect.collidepoint(event.pos):
                    ending()
                elif game_text_rect.collidepoint(event.pos):
                    return


def load_level(filename):
    with open('data/' + filename) as file:
        level = list(map(str.strip, file))
        max_len = len(max(level, key=len))
        level = list(map(lambda line: line.ljust(max_len, "."), level))
        return level


class Tile(pygame.sprite.Sprite):
    tile_images = {'floor': pygame.image.load('data/map_things_floor.jpg'),
                   'lukefloor': pygame.image.load('data/map_things_floor with luke.png'),
                   'wallblock': pygame.image.load('data/map_things_wall_block.png'),
                   'wallH': pygame.image.load('data/map_things_wall_H.jpg'),
                   'wall_': pygame.image.load('data/map_things_wall__.jpg'),
                   'wall]': pygame.image.load('data/map_things_wall_].jpg'),
                   'wall[': pygame.image.load('data/map_things_wall_[.jpg'),
                   'wallcornl': pygame.image.load('data/map_things_wall_cornleft.jpg'),
                   'wallcornr': pygame.image.load('data/map_things_wall_cornright.jpg'),
                   'wallupcornl': pygame.image.load('data/map_things_wall_upcornleft.jpg'),
                   'wallupcornr': pygame.image.load('data/map_things_wall_upcornright.jpg'),
                   'lukewall': pygame.image.load('data/map_things_wall with luke.jpg'),
                   'hole': pygame.image.load('data/map_things_hole.jpg')}

    def __init__(self, tile_type, x, y):
        super().__init__(all_sprites, tiles_group)
        self.image = Tile.tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height


class Player(pygame.sprite.Sprite):
    player_image = pygame.image.load('data/pix_mando_100.png')

    def __init__(self, level, x, y):
        super().__init__(all_sprites, player_group)
        self.x = x
        self.y = y
        self.level = level
        self.image = Player.player_image
        self.image_look = 'to right'
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width + (tile_width - self.rect.width) // 2
        self.rect.y = y * tile_height + (tile_width - self.rect.height) // 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.y != 0 and (self.level[self.y - 1][self.x] == 'O' or
                                                  self.level[self.y - 1][self.x] == ','):
            self.y -= 1
            self.rect.y -= tile_height
        if keys[pygame.K_s] and self.y != len(self.level) - 1 and (self.level[self.y + 1][self.x] == 'O' or
                                                                      self.level[self.y + 1][self.x] == '%' or
                                                                      self.level[self.y + 1][self.x] == ','):
            self.y += 1
            self.rect.y += tile_height
        if keys[pygame.K_a] and self.x != 0 and (self.level[self.y][self.x - 1] == "." or
                                                    self.level[self.y][self.x - 1] == "," or
                                                    self.level[self.y][self.x - 1] == '%' or
                                                    self.level[self.y][self.x - 1] == "P"):
            if self.image_look == 'to right':
                self.image = pygame.transform.flip(self.image, True, False)
                self.image_look = 'to left'
            self.x -= 1
            self.rect.x -= tile_width
        if keys[pygame.K_d] and self.x != len(self.level[0]) - 1 and (self.level[self.y][self.x + 1] == "." or
                                                                          self.level[self.y][self.x + 1] == "," or
                                                                          self.level[self.y][self.x + 1] == '%' or
                                                                          self.level[self.y][self.x + 1] == "P"):
            if self.image_look == 'to left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.image_look = 'to right'
            self.x += 1
            self.rect.x += tile_width


def create_level(filename):
    player = None
    level = load_level(filename)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('floor', x, y)
            elif level[y][x] == ',':
                Tile('lukefloor', x, y)
            elif level[y][x] == '%':
                Tile('lukewall', x, y)
            elif level[y][x] == '#':
                Tile('wallblock', x, y)
            elif level[y][x] == ']':
                Tile('wall]', x, y)
            elif level[y][x] == '[':
                Tile('wall[', x, y)
            elif level[y][x] == '_':
                Tile('wall_', x, y)
            elif level[y][x] == 'L':
                Tile('wallcornl', x, y)
            elif level[y][x] == 'R':
                Tile('wallcornr', x, y)
            elif level[y][x] == '>':
                Tile('wallupcornr', x, y)
            elif level[y][x] == '<':
                Tile('wallupcornl', x, y)
            elif level[y][x] == 'H':
                Tile('wallH', x, y)
            elif level[y][x] == 'O':
                Tile('hole', x, y)
            elif level[y][x] == 'P':
                Tile('floor', x, y)
                player = Player(level, x, y)
    return player


pygame.init()
size = width, height = 1400, 800
tile_width = 100
tile_height = 100
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Mandalorian')
clock = pygame.time.Clock()
FPS = 10
camera = Camera()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
intro()
player = create_level('level.txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ending()
    player_group.update()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill('black')
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
ending()

import sys

import pygame


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
    game_text = font.render('Play!', True, '#AF9898', '#594A51')
    exit_text = font.render('Exit', True, '#AF9898', '#594A51')
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
    with open('data/levels/' + filename) as file:
        level = list(map(str.strip, file))
        max_len = len(max(level, key=len))
        level = list(map(lambda line: line.ljust(max_len, "."), level))
        return level


class Tile(pygame.sprite.Sprite):
    tile_images = {'floor': pygame.image.load('data/map_things_10.png'),
                   'lukefloor': pygame.image.load('data/map_things_12.png'),
                   'wallblock': pygame.image.load('data/map_things_01.png'),
                   'wallH': pygame.image.load('data/map_things_03.png'),
                   'wall_': pygame.image.load('data/map_things_02.png'),
                   'wall]': pygame.image.load('data/map_things_08.png'),
                   'wall[': pygame.image.load('data/map_things_09.png'),
                   'wallcornl': pygame.image.load('data/map_things_07.png'),
                   'wallcornr': pygame.image.load('data/map_things_04.png'),
                   'wallupcornl': pygame.image.load('data/map_things_06.png'),
                   'wallupcornr': pygame.image.load('data/map_things_05.png'),
                   'lukewall': pygame.image.load('data/map_things_11.png'),
                   'hole': pygame.image.load('data/map_things_00.png')}

    def __init__(self, tile_type, x, y):
        if tile_type in ['floor', 'lukefloor', 'lukewall']:
            super().__init__(all_sprites, tiles_group, floors_group)
        else:
            super().__init__(all_sprites, tiles_group, walls_group)
        self.image = Tile.tile_images[tile_type]
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.tile = tile_type
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height


class BulletPlayer(pygame.sprite.Sprite):
    bulletimage = pygame.image.load('data/rsz_2unnamed.png')

    def __init__(self, x, y, facing):
        super().__init__(all_sprites, bullets_group)
        self.image = BulletPlayer.bulletimage
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.facing = facing
        self.speed = 60 * self.facing
        self.index = 0

    def update(self):
        self.rect = self.rect.move(self.speed, 0)
        if pygame.sprite.spritecollideany(self, walls_group):
            pygame.sprite.Sprite.remove(self, bullets_group)


class Player(pygame.sprite.Sprite):
    player_image = pygame.image.load('data/mando_00.png')

    def __init__(self, level, x, y):
        super().__init__(all_sprites, player_group)
        self.x = x
        self.y = y
        self.level = level
        self.image = Player.player_image
        self.image_look = 'to right'
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_width
        self.rect.y = y * tile_height
        self.spriteindex = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.y != 0 and (self.level[self.y - 1][self.x] == 'O' or
                                                 self.level[self.y - 1][self.x] == ','):
            self.image = pygame.image.load('data/mando_12.png')
            if self.image_look == 'to left':
                self.image = pygame.transform.flip(self.image, True, False)
            self.y -= 1
            self.rect.y -= tile_height
        if keys[pygame.K_s] and self.y != len(self.level) - 1 and (self.level[self.y + 1][self.x] == 'O' or
                                                                   self.level[self.y + 1][self.x] == '%'):
            self.image = pygame.image.load('data/mando_12.png')
            if self.image_look == 'to left':
                self.image = pygame.transform.flip(self.image, True, False)
            self.y += 1
            self.rect.y += tile_height
        if keys[pygame.K_a] and self.x != 0 and self.level[self.y][self.x] != 'O' and \
                (self.level[self.y][self.x - 1] == "." or
                 self.level[self.y][self.x - 1] == "," or
                 self.level[self.y][self.x - 1] == '%' or
                 self.level[self.y][self.x - 1] == "P"):
            self.image = pygame.image.load(MANDO_MOVE_SPRITES[(self.spriteindex + 1) % 4])
            self.image = pygame.transform.flip(self.image, True, False)
            self.spriteindex = (self.spriteindex + 1) % 4
            self.rect.x -= tile_width
            self.x -= 1
            self.image_look = 'to left'
        if keys[pygame.K_d] and self.x != len(self.level[0]) - 1 and self.level[self.y][self.x] != 'O' and \
                (self.level[self.y][self.x + 1] == "." or
                 self.level[self.y][self.x + 1] == "," or
                 self.level[self.y][self.x + 1] == '%' or
                 self.level[self.y][self.x + 1] == "P"):
            self.image = pygame.image.load(MANDO_MOVE_SPRITES[self.spriteindex])
            if self.image_look == 'to left':
                self.image = pygame.transform.flip(self.image, True, False)
            self.spriteindex = (self.spriteindex + 1) % 4
            self.rect.x += tile_width
            self.x += 1
            self.image_look = 'to right'
        elif not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.image = pygame.image.load('data/mando_00.png')
            if self.image_look == 'to left':
                self.image = pygame.transform.flip(self.image, True, False)
            self.spriteindex = 0

    def shoot(self):
        if self.image_look == 'to right':
            self.image = pygame.image.load('data/mando_02.png')
            bullet = BulletPlayer(self.rect.x + 50, self.rect.y, 1)
        elif self.image_look == 'to left':
            self.image = pygame.transform.flip(pygame.image.load('data/mando_02.png'), True, False)
            bullet = BulletPlayer(self.rect.x - 100, self.rect.y, -1)


'''class Enemy(pygame.sprite.Sprite):
    enemy_image = pygame.image.load('data/enemysprite.png')

    def __init__(self, level, x, y):
        super().__init__(all_sprites, enemy_group)
        self.x = x
        self.y = y
        self.level = level
        self.image = Enemy.enemy_image
        self.image_look = 'to left'''


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


LEVEL = f"level{int(input('Введите номер нужного уровня: '))}.txt"
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
walls_group = pygame.sprite.Group()
floors_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
MANDO_MOVE_SPRITES = ['data/mando_00.png', 'data/mando_04.png', 'data/mando_05.png', 'data/mando_06.png']
#try:
intro()
player = create_level(LEVEL)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ending()
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot()
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill('black')
    tiles_group.draw(screen)
    player_group.draw(screen)
    bullets_group.draw(screen)
    player_group.update()
    bullets_group.update()
    camera.update(player)
    pygame.display.flip()
    clock.tick(FPS)
#except:
#   ending()
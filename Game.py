import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "levels/" + filename
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(box_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Sky(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(sky_group, all_sprites)
        self.image = sky_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y - 19
        self.y_speed = 0
        self.x_speed = 0
        self.grav = 1
        self.jump = False
        self.sky = True

    def update(self):
        keys = pygame.key.get_pressed()
        v = 5

        if keys[pygame.K_RIGHT]:
            self.x_speed = v
        else:
            self.x_speed = 0

        if keys[pygame.K_UP]:
            self.jump = True

        if keys[pygame.K_LEFT]:
            self.x_speed = -v
        elif not keys[pygame.K_RIGHT]:
            self.x_speed = 0

        if self.jump and not self.sky:
            self.y_speed = -15
            self.collide(0, self.y_speed, box_group)

        if self.sky:
            self.y_speed += self.grav

        self.sky = True
        self.rect.y += self.y_speed
        self.collide(0, self.y_speed, box_group)

        self.rect.x += self.x_speed
        self.collide(self.x_speed, 0, box_group)

    def collide(self, x_speed, y_speed, box_group):
        for box in box_group:
            if pygame.sprite.collide_rect(self, box):
                if x_speed > 0:
                    self.rect.right = box.rect.left

                if x_speed < 0:
                    self.rect.left = box.rect.right

                if y_speed > 0:
                    self.rect.bottom = box.rect.top
                    self.sky = False
                    self.jump = False
                    self.y_speed = 0

                if y_speed < 0:
                    self.rect.top = box.rect.bottom
                    self.y_speed = 0


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
sky_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()

pygame.init()
size = width, height = 1000, 325
screen = pygame.display.set_mode(size)

FPS = 30
clock = pygame.time.Clock()
tile_images = {
    'wall': pygame.transform.scale(load_image('wall.png', -1), (25, 25)),
    'cloud': pygame.transform.scale(load_image('cloud.jpg'), (25, 25)),
}
sky_image = pygame.transform.scale(load_image('sky.png'), (25, 25))
player_image = load_image('mario.png', -1)

tile_width = tile_height = 25


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Sky(x, y)
            elif level[y][x] == '#':
                Box('wall', x, y)
            elif level[y][x] == '@':
                Sky(x, y)
                new_player = Player(x, y)
            elif level[y][x] == '%':
                Box('wall', x, y)
    return new_player, x, y


def game(screen):
    filename = 'level1.txt'
    if not os.path.exists('levels/' + filename):
        print(f"Файл с уровнем '{filename}' не найден")
        sys.exit()
    level = load_level(filename)
    player, level_x, level_y = generate_level(level)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill((0, 0, 0))
        player_group.update()
        sky_group.draw(screen)
        tiles_group.draw(screen)
        box_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


game(screen)

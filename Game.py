import os
import sys

import pygame


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
        self.image = mario_right_images['mario1']
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y - 19
        self.y_speed = 0
        self.x_speed = 0
        self.grav = 1
        self.jump = False
        self.sky = True
        self.state_move = 1
        self.side = 'right'
        self.on_bottom = True

    def update(self):
        keys = pygame.key.get_pressed()
        v = 5
        if keys[pygame.K_RIGHT]:
            if self.state_move < 0:
                self.state_move = 1
            if self.state_move == 1:
                self.image = mario_right_images['mario2']
                self.state_move = 2
            elif self.state_move == 2:
                self.image = mario_right_images['mario3']
                self.state_move = 3
            elif self.state_move == 3:
                self.image = mario_right_images['mario4']
                self.state_move = 1
            self.x_speed = v
            self.side = 'right'
        elif keys[pygame.K_LEFT]:
            if self.state_move > 0:
                self.state_move = -1
            if self.state_move == -1:
                self.image = mario_left_images['mario2']
                self.state_move = -2
            elif self.state_move == -2:
                self.image = mario_left_images['mario3']
                self.state_move = -3
            elif self.state_move == -3:
                self.image = mario_left_images['mario4']
                self.state_move = -1
            self.x_speed = -v
            self.side = 'left'
        else:
            if self.state_move >= 1:
                self.image = mario_right_images['mario1']
            elif self.state_move <= -1:
                self.image = mario_left_images['mario1']
            self.x_speed = 0

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            if self.side == 'right':
                self.image = mario_right_images['mario5']
            else:
                self.image = mario_left_images['mario5']
            self.state_move = 0
            self.on_bottom = False
            self.jump = True

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
                    if not self.on_bottom:
                        if self.side == 'right':
                            self.image = mario_right_images['mario1']
                            self.state_move = 1
                        else:
                            self.image = mario_left_images['mario1']
                            self.state_move = -1
                        self.on_bottom = True

                if y_speed < 0:
                    self.rect.top = box.rect.bottom
                    self.y_speed = 0


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
sky_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()

pygame.init()
pygame.mixer.init()
size = width, height = 1000, 325
screen = pygame.display.set_mode(size)

FPS = 30
clock = pygame.time.Clock()
tile_images = {
    'wall': pygame.transform.scale(load_image('wall.png', -1), (25, 25)),
    'cloud': pygame.transform.scale(load_image('sprites.png'), (100, 50)),
}
mario_right_images = {
    'mario1': pygame.transform.scale(load_image('mario1.png', -1), (20, 20)),
    'mario2': pygame.transform.scale(load_image('mario12.png', -1), (20, 20)),
    'mario3': pygame.transform.scale(load_image('mario13.png', -1), (20, 20)),
    'mario4': pygame.transform.scale(load_image('mario14.png', -1), (20, 20)),
    'mario5': pygame.transform.scale(load_image('mario15.png', -1), (20, 20))
}
mario_left_images = {
    'mario1': pygame.transform.scale(load_image('mario2.png', -1), (20, 20)),
    'mario2': pygame.transform.scale(load_image('mario22.png', -1), (20, 20)),
    'mario3': pygame.transform.scale(load_image('mario23.png', -1), (20, 20)),
    'mario4': pygame.transform.scale(load_image('mario24.png', -1), (20, 20)),
    'mario5': pygame.transform.scale(load_image('mario25.png'), (20, 20))
}
sky_image = pygame.transform.scale(load_image('sky.png'), (25, 25))

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
            elif level[y][x] == '!':
                Tile('cloud', x, y)
    return new_player, x, y


def music_level(music_name, music=True):
    try:
        pygame.mixer.music.load('sounds/' + music_name)
        if music:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)
        else:
            pygame.mixer.music.stop()
    except pygame.error:
        print('Не удалось загрузить звуковой файл')


def sound_level(sound_name, sfx=True):
    try:
        sound = pygame.mixer.Sound('sounds/' + sound_name)
        if sfx:
            sound.play()
            sound.set_volume(0.6)
        else:
            sound.stop()
    except pygame.error:
        print('Не удалось загрузить звуковой файл')


def game(screen, sfx=True):
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
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_SPACE):
                sound_level('sfx-13.mp3', sfx)
        screen.fill((0, 0, 0))
        player_group.update()
        sky_group.draw(screen)
        tiles_group.draw(screen)
        box_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

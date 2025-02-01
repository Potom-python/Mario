import os
import random
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


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coin_group, all_sprites)
        self.image = coin_images['coin1']
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.y_speed = -10
        self.start = pygame.time.get_ticks()
        self.exist = 500

    def update(self):
        if self.image == coin_images['coin1']:
            self.image = coin_images['coin2']
        elif self.image == coin_images['coin2']:
            self.image = coin_images['coin3']
        elif self.image == coin_images['coin3']:
            self.image = coin_images['coin4']
        else:
            self.image = coin_images['coin1']
        self.y_speed += 1
        self.rect.y += self.y_speed
        if pygame.time.get_ticks() - self.start >= self.exist:
            self.kill()


class LuckyBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(lucky_group, all_sprites)
        self.image = luckyblock_images['block1']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.last_change = pygame.time.get_ticks()
        self.inter = 200
        self.changed = False

    def update(self):
        if not self.changed:
            current = pygame.time.get_ticks()
            if current - self.last_change >= self.inter:
                self.last_change = current
                if self.image == luckyblock_images['block1']:
                    self.image = luckyblock_images['block2']
                elif self.image == luckyblock_images['block2']:
                    self.image = luckyblock_images['block3']
                else:
                    self.image = luckyblock_images['block1']
        else:
            self.image = luckyblock_images['block4']


class Camera:
    def __init__(self, width):
        self.width = width
        self.x = 0

    def apply(self, object):
        object.rect.x += self.x

    def update(self, target):

        self.x = -(target.rect.x + target.rect.w // 2 - self.width // 2)


class MagicMash(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(magic_mash_group, all_sprites)
        self.image = magic_mash_image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.x_speed = 3
        self.y_speed = 0
        self.grav = 0.5

    def update(self):
        self.apply_gravity()
        self.x_collisions(box_group)
        self.y_collisions(box_group)

    def apply_gravity(self):
        self.y_speed += self.grav

    def x_collisions(self, box_group):
        temp_rect = self.rect.copy()
        temp_rect.x += self.x_speed

        for box in box_group:
            if temp_rect.colliderect(box.rect):
               self.x_speed *= -1
               return

        self.rect.x += self.x_speed

    def y_collisions(self, box_group):
        temp_rect = self.rect.copy()
        temp_rect.y += self.y_speed

        for box in box_group:
            if temp_rect.colliderect(box.rect):
                if self.y_speed > 0:
                     self.rect.bottom = box.rect.top
                self.y_speed = 0
                return
        self.rect.y += self.y_speed


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = mario_right_images['mario1'][0]
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
        self.status = 0

    def update(self, sfx, number_level):
        keys = pygame.key.get_pressed()
        v = 5
        if keys[pygame.K_RIGHT]:
            if self.state_move < 0:
                self.state_move = 1
            if self.state_move == 1:
                self.image = mario_right_images['mario2'][self.status]
                self.state_move = 2
            elif self.state_move == 2:
                self.image = mario_right_images['mario3'][self.status]
                self.state_move = 3
            elif self.state_move == 3:
                self.image = mario_right_images['mario4'][self.status]
                self.state_move = 1
            self.x_speed = v
            self.side = 'right'
        elif keys[pygame.K_LEFT]:
            if self.state_move > 0:
                self.state_move = -1
            if self.state_move == -1:
                self.image = mario_left_images['mario2'][self.status]
                self.state_move = -2
            elif self.state_move == -2:
                self.image = mario_left_images['mario3'][self.status]
                self.state_move = -3
            elif self.state_move == -3:
                self.image = mario_left_images['mario4'][self.status]
                self.state_move = -1
            self.x_speed = -v
            self.side = 'left'
        else:
            if self.state_move >= 1:
                self.image = mario_right_images['mario1'][self.status]
            elif self.state_move <= -1:
                self.image = mario_left_images['mario1'][self.status]
            self.x_speed = 0

        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.jump = True
        if self.jump:
            if self.side == 'right':
                self.image = mario_right_images['mario5'][self.status]
            else:
                self.image = mario_left_images['mario5'][self.status]
            self.state_move = 0
            self.on_bottom = False

        if self.jump and not self.sky:
            self.y_speed = -15
            self.collide(0, self.y_speed, box_group)
            sound_level('sfx-13.mp3', sfx)

        if self.sky:
            self.y_speed += self.grav

        self.sky = True
        self.rect.y += self.y_speed
        self.collide(0, self.y_speed, box_group)

        self.rect.x += self.x_speed
        if self.rect.x < 0:
            self.rect.x = 0
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
                            self.image = mario_right_images['mario1'][self.status]
                            self.state_move = 1
                        else:
                            self.image = mario_left_images['mario1'][self.status]
                            self.state_move = -1
                        self.on_bottom = True

                if y_speed < 0:
                    self.rect.top = box.rect.bottom
                    self.y_speed = 0

        for lucky in lucky_group:
            if pygame.sprite.collide_rect(self, lucky):
                if x_speed > 0:
                    self.rect.right = lucky.rect.left

                if x_speed < 0:
                    self.rect.left = lucky.rect.right

                if y_speed > 0:
                    self.rect.bottom = lucky.rect.top
                    self.sky = False
                    self.jump = False
                    self.y_speed = 0
                    if not self.on_bottom:
                        if self.side == 'right':
                            self.image = mario_right_images['mario1'][self.status]
                            self.state_move = 1
                        else:
                            self.image = mario_left_images['mario1'][self.status]
                            self.state_move = -1
                        self.on_bottom = True

                if y_speed < 0:
                    if not lucky.changed:
                        sound_level('sfx-5.mp3')
                        Coin(lucky.rect.centerx, lucky.rect.centery)
                        MagicMash(lucky.rect.centerx, lucky.rect.centery)
                    lucky.changed = True
                    self.rect.top = lucky.rect.bottom
                    self.y_speed = 0

        for mash in magic_mash_group:
            if pygame.sprite.collide_rect(self, mash):
                cordx = self.rect.x
                sound_level('sfx-7.mp3')
                self.status = 1
                self.rect = mario_right_images['mario1'][self.status].get_rect()
                self.rect.bottom = mash.rect.bottom
                self.rect.x = cordx

                mash.kill()


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
sky_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
lucky_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
magic_mash_group = pygame.sprite.Group()

pygame.init()
pygame.mixer.init()
size = width, height = 1000, 325
screen = pygame.display.set_mode(size)

FPS = 30
clock = pygame.time.Clock()
tile_images = {
    'wall': pygame.transform.scale(load_image('wall.png', -1), (25, 25)),
    'column1': pygame.transform.scale(load_image('column1.png'), (50, 60)),
    'cloud1': pygame.transform.scale(load_image('cloud1.png'), (100, 50)),
    'cloud2': pygame.transform.scale(load_image('cloud2.png'), (70, 50)),
    'grass1': pygame.transform.scale(load_image('grass1.png'), (100, 50)),
    'grass2': pygame.transform.scale(load_image('grass1.png'), (100, 50))
}
mario_right_images = {
    'mario1': [pygame.transform.scale(load_image('mario1.png', -1), (20, 20)), pygame.transform.scale(load_image('b_mario1.png', -1), (30, 50))],
    'mario2': [pygame.transform.scale(load_image('mario12.png', -1), (20, 20)), pygame.transform.scale(load_image('b_mario12.png', -1), (30, 50))],
    'mario3': [pygame.transform.scale(load_image('mario13.png', -1), (20, 20)), pygame.transform.scale(load_image('b_mario13.png', -1), (30, 50))],
    'mario4': [pygame.transform.scale(load_image('mario14.png', -1), (20, 20)), pygame.transform.scale(load_image('b_mario14.png', -1), (30, 50))],
    'mario5': [pygame.transform.scale(load_image('mario15.png', -1), (20, 20)), pygame.transform.scale(load_image('b_mario15.png', -1), (30, 50))]
}
mario_left_images = {
    'mario1': [pygame.transform.scale(load_image('mario2.png', -1), (20, 20)), pygame.transform.scale(load_image('b_mario2.png', -1), (30, 50))],
    'mario2': [pygame.transform.scale(load_image('mario22.png', -1), (20, 20)), pygame.transform.scale(load_image('b_mario22.png', -1), (30, 50))],
    'mario3': [pygame.transform.scale(load_image('mario23.png', -1), (20, 20)), pygame.transform.scale(load_image('b_mario23.png', -1), (30, 50))],
    'mario4': [pygame.transform.scale(load_image('mario24.png', -1), (20, 20)), pygame.transform.scale(load_image('b_mario24.png', -1), (30, 50))],
    'mario5': [pygame.transform.scale(load_image('mario25.png'), (20, 20)), pygame.transform.scale(load_image('b_mario25.png', -1), (30, 50))]
}
luckyblock_images = {
    'block1': pygame.transform.scale(load_image('luckyblock1.png', -1), (25, 25)),
    'block2': pygame.transform.scale(load_image('luckyblock2.png', -1), (25, 25)),
    'block3': pygame.transform.scale(load_image('luckyblock3.png', -1), (25, 25)),
    'block4': pygame.transform.scale(load_image('changed_lucky_block.png', -1), (25, 25))
}
sky_image = pygame.transform.scale(load_image('sky.png'), (25, 25))
magic_mash_image = pygame.transform.scale(load_image('magic_mashroom.png'), (25, 25))
coin_images = {
    'coin1': pygame.transform.scale(load_image('coin1.png'), (15, 20)),
    'coin2': pygame.transform.scale(load_image('coin2.png'), (15, 20)),
    'coin3': pygame.transform.scale(load_image('coin3.png'), (15, 20)),
    'coin4': pygame.transform.scale(load_image('coin4.png'), (15, 20))
}

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
                Sky(x, y)
                Tile(random.choice(['cloud1', 'cloud2']), x, y)
            elif level[y][x] == '?':
                LuckyBlock(x, y)
            elif level[y][x] == ',':
                Sky(x, y)
                Tile(random.choice(['grass1', 'grass2']), x, y)
            elif level[y][x] == '|':
                Sky(x, y)
                Box('column1', x, y)
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


def pause_menu(sfx):
    paused = True
    background = screen.copy()
    sound_level('sfx-1.mp3', sfx)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                elif event.key == pygame.K_q:
                    terminate()
        screen.blit(background, (0, 0))

        font = pygame.font.SysFont(None, 40)
        text = font.render('Пауза', True, (0, 255, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2 - 20))
        screen.blit(text, text_rect)

        continue_text = font.render('Нажмите ESC для продолжения', True, (0, 255, 0))
        continue_rect = continue_text.get_rect(center=(width // 2, height // 2 + 20))
        screen.blit(continue_text, continue_rect)

        exit_text = font.render('Нажмите Q для выхода из игры', True, (0, 255, 0))
        exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 60))
        screen.blit(exit_text, exit_rect)

        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen():
    background = screen.copy()
    font = pygame.font.SysFont(None, 55)

    game_over_text = font.render('GAME OVER', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 20))

    restart_text = font.render('Нажмите R для перезапуска', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 20))

    exit_text = font.render('Нажмите Q для выхода', True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 60))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    screen.fill((0, 0, 0))
                    background.fill((0, 0, 0))
                    return 2

                elif event.key == pygame.K_q:
                    terminate()

        screen.blit(background, (0, 0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(exit_text, exit_rect)

        pygame.display.flip()
        clock.tick(FPS)


def game(screen, number_level, sfx=True):
    filename = number_level
    if not os.path.exists('levels/' + filename):
        print(f"Файл с уровнем '{filename}' не найден")
        sys.exit()
    level = load_level(filename)
    player, level_x, level_y = generate_level(level)
    camera = Camera(width)

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu(sfx)

        if not game_over:
            screen.fill((0, 0, 0))
            player_group.update(sfx, number_level)
            camera.update(player)
            lucky_group.update()
            coin_group.update()
            magic_mash_group.update()
            for sprite in all_sprites:
                camera.apply(sprite)
            sky_group.draw(screen)
            coin_group.draw(screen)
            tiles_group.draw(screen)
            magic_mash_group.draw(screen)
            lucky_group.draw(screen)
            box_group.draw(screen)
            player_group.draw(screen)

            if player.rect.y + player.rect.h >= height:
                sound_level('mario-smert.mp3')
                game_over = True

        else:
            game_over = game_over_screen()
            if game_over == 2:
                size_game = 1000, 325
                screen_game = pygame.display.set_mode(size_game)
                game(screen_game, number_level, sfx)
                return

        pygame.display.flip()
        clock.tick(FPS)
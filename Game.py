import os
import random
import sys

import pygame

COINS = 0
start_time = 0
TIME = TIME_REMAINING = 250000
SCORE = 0


# функция выхода из игры
def terminate():
    pygame.quit()
    sys.exit()


# функция загрузки изображений
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


# функция для загрузки уровней
def load_level(filename):
    filename = "levels/" + filename
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


# функция спавна монет и магических грибов
def coin_or_mash(x, y, bottom):
    chance = random.randint(0, 5)
    if chance != 5:
        sound_level('sfx-5.mp3')
        Coin(x, y)
        return 1
    else:
        sound_level('sfx-7.mp3')
        MagicMash(x, y, bottom)
        return 0


# класс, реализующий финиш игрового процесса
class Finish(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(finish_group, all_sprites)
        self.image = finish_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# класс, реализующий статические объекты декорации
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# класс, реализующий стандартные блоки и столбы
class Box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(box_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# класс реализующий небо
class Sky(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(sky_group, all_sprites)
        self.image = sky_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# класс реализующий монету
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coin_group, all_sprites)
        self.image = coin_images['coin1']
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.y_speed = -15
        self.start = pygame.time.get_ticks()
        self.exist = 900
        self.last_change = pygame.time.get_ticks()
        self.inter = 200

    def update(self):
        current = pygame.time.get_ticks()
        if current - self.last_change >= self.inter:
            self.last_change = current
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


# класс, реализующий лакиблок при уничтожении которого, появляется либо монета, либо магический гриб
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


# класс, реализующий файрбол, который уничтожает врагов
class FireBall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, side):
        super().__init__(fireball_group, all_sprites)
        self.image = fire_ball_images['fireball1']
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.x_speed = 7 if side == 'right' else -7
        self.y_speed = 5
        self.last_change = pygame.time.get_ticks()
        self.inter = 50
        self.grav = 1
        self.collide = False

    def update(self):
        current = pygame.time.get_ticks()
        if current - self.last_change >= self.inter:
            self.last_change = current
            if not self.collide:
                if self.image == fire_ball_images['fireball1']:
                    self.image = fire_ball_images['fireball2']
                elif self.image == fire_ball_images['fireball2']:
                    self.image = fire_ball_images['fireball3']
                elif self.image == fire_ball_images['fireball3']:
                    self.image = fire_ball_images['fireball4']
                else:
                    self.image = fire_ball_images['fireball1']
            else:
                if self.image == fire_ball_images['fireball5']:
                    self.image = fire_ball_images['fireball6']
                elif self.image == fire_ball_images['fireball6']:
                    self.image = fire_ball_images['fireball7']
                else:
                    self.kill()

        self.apply_gravity()
        self.x_collisions()
        self.y_collisions()
        self.enemy_collisions()

    def apply_gravity(self):
        self.y_speed += self.grav

    def x_collisions(self):
        temp_rect = self.rect.copy()
        temp_rect.x += self.x_speed

        if not self.collide:

            for box in box_group:
                if temp_rect.colliderect(box.rect):
                    self.collide = True
                    self.image = fire_ball_images['fireball5']

            for lucky in lucky_group:
                if temp_rect.colliderect(lucky.rect):
                    self.collide = True
                    self.image = fire_ball_images['fireball5']

            self.rect.x += self.x_speed

    def y_collisions(self):
        temp_rect = self.rect.copy()
        temp_rect.y += self.y_speed

        for box in box_group:
            if temp_rect.colliderect(box.rect):
                if self.y_speed > 0:
                    self.y_speed = - 5
                else:
                    self.y_speed = 5
                return

        for lucky in lucky_group:
            if temp_rect.colliderect(lucky.rect):
                if self.y_speed > 0:
                    self.y_speed = -5
                else:
                    self.y_speed = 5
                return

        self.rect.y += self.y_speed

    def enemy_collisions(self):
        global SCORE
        if not self.collide:
            for enemy in enemy_group:
                if self.rect.colliderect(enemy.rect):
                    if isinstance(enemy, Goombas):
                        SCORE += 100
                    else:
                        SCORE += 200
                    self.collide = True
                    enemy.death()
                    self.image = fire_ball_images['fireball5']


# класс, реализующий камеру, которая фокусируется на главном герое
class Camera:
    def __init__(self, width):
        self.width = width
        self.x = 0

    def apply(self, object):
        object.rect.x += self.x

    def update(self, target):
        self.x = -(target.rect.x + target.rect.w // 2 - self.width // 2)


# класс, реализующий магичсекий гриб, при съедении которого, главный герой становится сильнее
class MagicMash(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, bottom):
        super().__init__(magic_mash_group, all_sprites)
        self.image = magic_mash_image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.rect.bottom = bottom
        self.x_speed = 3
        self.y_speed = 0
        self.grav = 0.5

    def update(self):
        self.apply_gravity()
        self.x_collisions(box_group, lucky_group)
        self.y_collisions(box_group, lucky_group)

    def apply_gravity(self):
        self.y_speed += self.grav

    def x_collisions(self, box_group, lucky_group):
        temp_rect = self.rect.copy()
        temp_rect.x += self.x_speed

        for box in box_group:
            if temp_rect.colliderect(box.rect):
                self.x_speed *= -1
                return

        for lucky in lucky_group:
            if temp_rect.colliderect(lucky.rect):
                self.x_speed *= -1
                return

        self.rect.x += self.x_speed

    def y_collisions(self, box_group, lucky_group):
        temp_rect = self.rect.copy()
        temp_rect.y += self.y_speed

        for box in box_group:
            if temp_rect.colliderect(box.rect):
                if self.y_speed > 0:
                    self.rect.bottom = box.rect.top
                self.y_speed = 0
                return

        for lucky in lucky_group:
            if temp_rect.colliderect(lucky.rect):
                if self.y_speed > 0:
                    self.rect.bottom = lucky.rect.top
                self.y_speed = 0
                return

        self.rect.y += self.y_speed


# класс, реализующий моба "goombas", он является одним из врагов главного героя
class Goombas(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(goombas_group, all_sprites, enemy_group)
        self.image = goombas_images['goombas1']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x_speed = -2
        self.y_speed = 0
        self.grav = 0.5
        self.last_change = pygame.time.get_ticks()
        self.inter = 150

    def update(self):
        current = pygame.time.get_ticks()
        if current - self.last_change >= self.inter:
            self.last_change = current
            if self.image == goombas_images['goombas1']:
                self.image = goombas_images['goombas2']
            else:
                self.image = goombas_images['goombas1']
        self.apply_gravity()
        self.x_collisions(box_group, lucky_group)
        self.y_collisions(box_group, lucky_group)

    def apply_gravity(self):
        self.y_speed += self.grav

    def x_collisions(self, box_group, lucky_group):
        temp_rect = self.rect.copy()
        temp_rect.x += self.x_speed

        for box in box_group:
            if temp_rect.colliderect(box.rect):
                self.x_speed *= -1
                return

        for lucky in lucky_group:
            if temp_rect.colliderect(lucky.rect):
                self.x_speed *= -1
                return

        self.rect.x += self.x_speed

    def y_collisions(self, box_group, lucky_group):
        temp_rect = self.rect.copy()
        temp_rect.y += self.y_speed

        for box in box_group:
            if temp_rect.colliderect(box.rect):
                if self.y_speed > 0:
                    self.rect.bottom = box.rect.top
                self.y_speed = 0
                return

        for lucky in lucky_group:
            if temp_rect.colliderect(lucky.rect):
                if self.y_speed > 0:
                    self.rect.bottom = lucky.rect.top
                self.y_speed = 0
                return
        self.rect.y += self.y_speed

    def death(self):
        self.kill()


# класс, реализующий моба "koopas", он является одним из врагов главного героя
class Koopas(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(koopas_group, all_sprites, enemy_group)
        self.image = koopas_images['koopas1']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x_speed = -2
        self.y_speed = 0
        self.grav = 0.5
        self.last_change = pygame.time.get_ticks()
        self.inter = 150
        self.side = 'left'
        self.state = 0

    def update(self):
        if not self.state:
            current = pygame.time.get_ticks()
            if current - self.last_change >= self.inter:
                self.last_change = current
                self.animate()

            self.apply_gravity()
            self.x_collisions(box_group, lucky_group)
            self.y_collisions(box_group, lucky_group)
        else:
            self.image = koopas_images['koopas5']

    def animate(self):

        if self.side == 'left':
            if self.image == koopas_images['koopas1']:
                self.image = koopas_images['koopas2']
            else:
                self.image = koopas_images['koopas1']
        else:
            if self.image == koopas_images['koopas3']:
                self.image = koopas_images['koopas4']
            else:
                self.image = koopas_images['koopas3']

    def apply_gravity(self):
        self.y_speed += self.grav

    def x_collisions(self, box_group, lucky_group):
        temp_rect = self.rect.copy()
        temp_rect.x += self.x_speed

        for box in box_group:
            if temp_rect.colliderect(box.rect):
                self.x_speed *= -1
                if self.side == 'left':
                    self.side = 'right'
                    self.image = koopas_images['koopas3']
                else:
                    self.side = 'left'
                    self.image = koopas_images['koopas1']
                return

        for lucky in lucky_group:
            if temp_rect.colliderect(lucky.rect):
                self.x_speed *= -1
                if self.side == 'left':
                    self.side = 'right'
                    self.image = koopas_images['koopas3']
                else:
                    self.side = 'left'
                    self.image = koopas_images['koopas1']
                return

        self.rect.x += self.x_speed

    def y_collisions(self, box_group, lucky_group):
        temp_rect = self.rect.copy()
        temp_rect.y += self.y_speed

        for box in box_group:
            if temp_rect.colliderect(box.rect):
                if self.y_speed > 0:
                    self.rect.bottom = box.rect.top
                self.y_speed = 0
                return

        for lucky in lucky_group:
            if temp_rect.colliderect(lucky.rect):
                if self.y_speed > 0:
                    self.rect.bottom = lucky.rect.top
                self.y_speed = 0
                return
        self.rect.y += self.y_speed

    def death(self):
        self.kill()


# класс, реализующий главного героя
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
        self.invulnerability = False
        self.key_pressed = False
        self.over = False

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

        if keys[pygame.K_c]:
            if not self.key_pressed:
                sound_level('sfx-17.mp3', sfx)
                FireBall(self.rect.centerx, self.rect.centery, self.side)
                self.key_pressed = True
        else:
            self.key_pressed = False

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
            self.collide(0, self.y_speed, sfx)
            if self.status:
                sound_level('smb_jump-super.wav', sfx)
            else:
                sound_level('sfx-13.mp3', sfx)

        if self.sky:
            self.y_speed += self.grav

        for i in finish_group:
            if pygame.sprite.collide_rect(self, i):
                game_winner_screen()

        self.sky = True
        self.rect.y += self.y_speed
        self.collide(0, self.y_speed, sfx)

        self.rect.x += self.x_speed
        if self.rect.x < 0:
            self.rect.x = 0
        self.collide(self.x_speed, 0, sfx)

    def collide(self, x_speed, y_speed, sfx):
        global COINS
        global SCORE

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
                        COINS += coin_or_mash(lucky.rect.centerx, lucky.rect.centery, lucky.rect.top)
                    lucky.changed = True
                    self.rect.top = lucky.rect.bottom
                    self.y_speed = 0

        for mash in magic_mash_group:
            if pygame.sprite.collide_rect(self, mash):
                sound_level('sfx-10.mp3', sfx)
                cordx = self.rect.x
                bottom = self.rect.bottom
                self.status = 1
                self.rect = mario_right_images['mario1'][self.status].get_rect()
                self.rect.bottom = bottom
                self.rect.x = cordx
                SCORE += 1000

                mash.kill()

        for goom in goombas_group:
            if pygame.sprite.collide_rect(self, goom):
                if self.rect.bottom >= goom.rect.top and self.sky and y_speed > 0:
                    goom.death()
                    sound_level('smb_kick.wav', sfx)
                    self.y_speed = -5
                    self.sky = False
                    self.on_bottom = False
                    self.jump = False
                    SCORE += 100
                elif not self.invulnerability:
                    if self.status:
                        sound_level('get_hit.mp3', sfx)
                        cordx = self.rect.x
                        bottom = self.rect.bottom
                        self.status = 0
                        self.rect = mario_right_images['mario1'][self.status].get_rect()
                        self.rect.bottom = bottom
                        self.rect.x = cordx
                        self.set_invulnerability(2000)
                    else:
                        self.over = True

        for koop in koopas_group:
            if pygame.sprite.collide_rect(self, koop):
                if not koop.state:
                    if self.rect.bottom >= koop.rect.top and self.sky and y_speed > 0:
                        self.rect.bottom = koop.rect.top
                        koop.state = 1
                        sound_level('smb_kick.wav', sfx)
                        self.y_speed = -5
                        self.sky = False
                        self.on_bottom = False
                        self.jump = False

                    elif not self.invulnerability:
                        if self.status:
                            sound_level('get_hit.mp3', sfx)
                            cordx = self.rect.x
                            bottom = self.rect.bottom
                            self.status = 0
                            self.rect = mario_right_images['mario1'][self.status].get_rect()
                            self.rect.bottom = bottom
                            self.rect.x = cordx
                            self.set_invulnerability(2000)
                        else:
                            self.over = True
                else:
                    if self.rect.bottom >= koop.rect.top and self.sky and y_speed > 0:
                        self.rect.bottom = koop.rect.top
                        koop.state = 0
                        sound_level('smb_kick.wav', sfx)
                        self.y_speed = -5
                        self.sky = False
                        self.on_bottom = False
                        self.jump = False

                    if x_speed > 0:
                        self.rect.right = koop.rect.left

                    if x_speed < 0:
                        self.rect.left = koop.rect.right

    def set_invulnerability(self, time):
        self.invulnerability = True
        pygame.time.set_timer(pygame.USEREVENT, time)

    def make_invulnerability(self):
        self.invulnerability = False


# функция загрузки игры
def draw_game():
    global all_sprites, tiles_group, player_group, sky_group, box_group, lucky_group, coin_group, magic_mash_group
    global goombas_group, fireball_group, width, height, size, screen, FPS, clock, tile_images, mario_right_images
    global mario_left_images, luckyblock_images, sky_image, magic_mash_image, coin_images, goombas_images
    global fire_ball_images, tile_width, tile_height, finish_image, finish_group, koopas_images, koopas_group, enemy_group
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    sky_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    lucky_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    magic_mash_group = pygame.sprite.Group()
    goombas_group = pygame.sprite.Group()
    fireball_group = pygame.sprite.Group()
    finish_group = pygame.sprite.Group()
    koopas_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

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
        'mario1': [pygame.transform.scale(load_image('mario1.png', -1), (20, 20)),
                   pygame.transform.scale(load_image('b_mario1.png', -1), (30, 50))],
        'mario2': [pygame.transform.scale(load_image('mario12.png', -1), (20, 20)),
                   pygame.transform.scale(load_image('b_mario12.png', -1), (30, 50))],
        'mario3': [pygame.transform.scale(load_image('mario13.png', -1), (20, 20)),
                   pygame.transform.scale(load_image('b_mario13.png', -1), (30, 50))],
        'mario4': [pygame.transform.scale(load_image('mario14.png', -1), (20, 20)),
                   pygame.transform.scale(load_image('b_mario14.png', -1), (30, 50))],
        'mario5': [pygame.transform.scale(load_image('mario15.png', -1), (20, 20)),
                   pygame.transform.scale(load_image('b_mario15.png', -1), (30, 50))]
    }
    mario_left_images = {
        'mario1': [pygame.transform.scale(load_image('mario2.png', -1), (20, 20)),
                   pygame.transform.scale(load_image('b_mario2.png', -1), (30, 50))],
        'mario2': [pygame.transform.scale(load_image('mario22.png', -1), (20, 20)),
                   pygame.transform.scale(load_image('b_mario22.png', -1), (30, 50))],
        'mario3': [pygame.transform.scale(load_image('mario23.png', -1), (20, 20)),
                   pygame.transform.scale(load_image('b_mario23.png', -1), (30, 50))],
        'mario4': [pygame.transform.scale(load_image('mario24.png', -1), (20, 20)),
                   pygame.transform.scale(load_image('b_mario24.png', -1), (30, 50))],
        'mario5': [pygame.transform.scale(load_image('mario25.png'), (20, 20)),
                   pygame.transform.scale(load_image('b_mario25.png', -1), (30, 50))]
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
    goombas_images = {
        'goombas1': pygame.transform.scale(load_image('goombas1.png'), (25, 25)),
        'goombas2': pygame.transform.scale(load_image('goombas2.png'), (25, 25)),
    }
    koopas_images = {
        'koopas1': pygame.transform.scale(load_image('koopas1.png'), (30, 30)),
        'koopas2': pygame.transform.scale(load_image('koopas2.png'), (30, 30)),
        'koopas3': pygame.transform.scale(load_image('koopas3.png'), (30, 30)),
        'koopas4': pygame.transform.scale(load_image('koopas4.png'), (30, 30)),
        'koopas5': pygame.transform.scale(load_image('koopas5.png'), (30, 30))
    }
    fire_ball_images = {
        'fireball1': pygame.transform.scale(load_image('fireball1.png'), (10, 10)),
        'fireball2': pygame.transform.scale(load_image('fireball2.png'), (10, 10)),
        'fireball3': pygame.transform.scale(load_image('fireball3.png'), (10, 10)),
        'fireball4': pygame.transform.scale(load_image('fireball4.png'), (10, 10)),
        'fireball5': pygame.transform.scale(load_image('fireball5.png'), (10, 10)),
        'fireball6': pygame.transform.scale(load_image('fireball6.png'), (15, 15)),
        'fireball7': pygame.transform.scale(load_image('fireball7.png'), (20, 20))
    }
    finish_image = pygame.transform.scale(load_image('finish.png'), (75, 75))
    tile_width = tile_height = 25


# фунцкия, обрабатывающая столкноения мобов между собой
def one_group_collisions(group):
    sprites = group.sprites()

    for k in range(len(sprites)):
        for i in range(k + 1, len(sprites)):
            sprite1 = sprites[k]
            sprite2 = sprites[i]

            if pygame.sprite.collide_rect(sprite1, sprite2):
                if isinstance(sprite1, Koopas):
                    if sprite1.side == 'left':
                        sprite1.side = 'right'
                    else:
                        sprite1.side = 'left'
                if isinstance(sprite2, Koopas):
                    if sprite2.side == 'left':
                        sprite2.side = 'right'
                    else:
                        sprite2.side = 'left'
                sprite1.x_speed = -sprite1.x_speed
                sprite2.x_speed = -sprite2.x_speed


# функция генерации уровня
def generate_level(level):
    new_player, x = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Sky(x, y)
            elif level[y][x] == '#':
                Box('wall', x, y)
            elif level[y][x] == '@':
                Sky(x, y)
                new_player = Player(x, y)
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
            elif level[y][x] == '1':
                Sky(x, y)
                Goombas(x, y)
            elif level[y][x] == '2':
                Sky(x, y)
                Koopas(x, y)
            elif level[y][x] == '=':
                Sky(x, y)
                Finish(x, y)
    return new_player, x * tile_width


# функция для проигрывания музыки
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


# функция для проигрывания ивент-звука
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


# функция, реализующая паузу
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
        text = font.render('Пауза', True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2 - 20))
        screen.blit(text, text_rect)

        continue_text = font.render('Нажмите ESC для продолжения', True, (0, 0, 0))
        continue_rect = continue_text.get_rect(center=(width // 2, height // 2 + 20))
        screen.blit(continue_text, continue_rect)

        exit_text = font.render('Нажмите Q для выхода из игры', True, (0, 0, 0))
        exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 60))
        screen.blit(exit_text, exit_rect)

        pygame.display.flip()
        clock.tick(FPS)


# функция, рисующая экран победы
def game_winner_screen():
    background = screen.copy()
    font = pygame.font.SysFont(None, 55)

    winner_over_text = font.render('WINNER', True, (0, 255, 0))
    winner_over_rect = winner_over_text.get_rect(center=(width // 2, height // 2 - 20))

    exit_text = font.render('Нажмите Q для выхода', True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 60))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    terminate()

        screen.blit(background, (0, 0))
        screen.blit(winner_over_text, winner_over_rect)
        screen.blit(exit_text, exit_rect)

        pygame.display.flip()
        clock.tick(FPS)


# функция, рисующая экран смерти
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


# основная функция этого файла
def game(screen, number_level, sfx=True):
    draw_game()

    global COINS, SCORE, start_time, TIME, TIME_REMAINING
    filename = number_level
    if not os.path.exists('levels/' + filename):
        print(f"Файл с уровнем '{filename}' не найден")
        sys.exit()
    level = load_level(filename)
    player, level_x = generate_level(level)
    camera = Camera(width)

    game_over = False
    start = False

    def statistic():
        color = (255, 255, 255)
        font = pygame.font.SysFont(None, 30)
        coins_text = font.render('COINS', True, (color))
        coins_text_rect = coins_text.get_rect(center=(width // 3, 20))

        coins = font.render(str(COINS), True, (color))
        coins_rect = coins.get_rect(center=(width // 3, 40))

        time_text = font.render('TIME', True, (color))
        time_text_rect = time_text.get_rect(center=(width // 2, 20))

        time = font.render(str(TIME_REMAINING), True, (color))
        time_rect = time.get_rect(center=(width // 2, 40))

        score_text = font.render('SCORE', True, (color))
        score_text_rect = score_text.get_rect(center=(width // 3 * 2, 20))

        score = font.render(str(SCORE), True, (color))
        score_rect = score.get_rect(center=(width // 3 * 2, 40))

        screen.blit(coins_text, coins_text_rect)
        screen.blit(coins, coins_rect)
        screen.blit(time_text, time_text_rect)
        screen.blit(time, time_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(score, score_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu(sfx)
            if event.type == pygame.USEREVENT:
                player.make_invulnerability()

        if not start:
            start_time = pygame.time.get_ticks()
            start = True
        current_time = pygame.time.get_ticks()
        different = current_time - start_time
        TIME_REMAINING = (TIME - different) // 1000

        if different >= TIME:
            sound_level('mario-smert.mp3')
            COINS = 0
            SCORE = 0
            game_over = True

        if not game_over:
            screen.fill((0, 0, 0))
            player_group.update(sfx, number_level)
            camera.update(player)
            lucky_group.update()
            coin_group.update()
            magic_mash_group.update()
            one_group_collisions(enemy_group)
            enemy_group.update()
            fireball_group.update()
            for sprite in all_sprites:
                camera.apply(sprite)
            sky_group.draw(screen)
            finish_group.draw(screen)
            tiles_group.draw(screen)
            coin_group.draw(screen)
            magic_mash_group.draw(screen)
            enemy_group.draw(screen)
            lucky_group.draw(screen)
            box_group.draw(screen)
            fireball_group.draw(screen)
            player_group.draw(screen)
            statistic()

            if player.rect.y + player.rect.h >= height or player.over:
                sound_level('mario-smert.mp3')
                COINS = 0
                SCORE = 0
                game_over = True

        else:
            game_over = game_over_screen()
            if game_over == 2:
                screen.fill((255, 255, 255))
                size_game = 1000, 325
                screen_game = pygame.display.set_mode(size_game)
                draw_game()
                game(screen_game, number_level, sfx)

        pygame.display.flip()
        clock.tick(FPS)
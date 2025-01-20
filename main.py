import pygame
import sys
import os

pygame.init()
FPS = 30
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


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


class Button_def(pygame.sprite.Sprite):
    def __init__(self, top, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("button_grey.png", -1), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.top = top


class Button_anim(pygame.sprite.Sprite):
    def __init__(self, top, *group):
        super().__init__(*group)
        self.schet_anim = 0
        self.image = pygame.transform.scale(load_image("button_green.png", -1), (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.top = top


def start_screen():
    intro_text = ["Игра про марио", "",
                  "Перемещение героя происходит по нажатию стрелочек",
                  "Перемещение по меню с помощью стрелочек, чтобы выбрать enter", "",
                  "Играть",
                  "Настройки",
                  "Выход"]
    fon = pygame.transform.scale(load_image('fon_mar.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    schet_anim = 0
    buttons_sprites = pygame.sprite.Group()
    for line in intro_text[:5]:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    for line in intro_text[5:]:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        Button_def(text_coord, buttons_sprites)
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    Button_anim(210, buttons_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    schet_anim -= 1
                    if schet_anim == 0 or schet_anim == -3:
                        Button_def(240, buttons_sprites)
                        Button_anim(210, buttons_sprites)
                    elif schet_anim == 1 or schet_anim == -2:
                        Button_def(270, buttons_sprites)
                        Button_anim(240, buttons_sprites)
                    elif schet_anim == 2 or schet_anim == -1:
                        Button_def(210, buttons_sprites)
                        Button_anim(270, buttons_sprites)
                    else:
                        schet_anim = -1
                        Button_def(210, buttons_sprites)
                        Button_anim(270, buttons_sprites)
                elif event.key == pygame.K_DOWN:
                    schet_anim += 1
                    if schet_anim == 0 or schet_anim == -3:
                        Button_def(270, buttons_sprites)
                        Button_anim(210, buttons_sprites)
                    elif schet_anim == 1 or schet_anim == -2:
                        Button_def(210, buttons_sprites)
                        Button_anim(240, buttons_sprites)
                    elif schet_anim == 2 or schet_anim == -1:
                        Button_def(240, buttons_sprites)
                        Button_anim(270, buttons_sprites)
                    else:
                        Button_def(270, buttons_sprites)
                        Button_anim(210, buttons_sprites)
                        schet_anim = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if schet_anim == 0 or schet_anim == -3:
                    pass
                elif schet_anim == 1 or schet_anim == -2:
                    pass
                elif schet_anim == 2 or schet_anim == -1:
                    terminate()
            buttons_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


start_screen()

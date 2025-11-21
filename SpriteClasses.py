import pygame
import json
import os


pygame.init()
pygame.font.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SpikeLeft(pygame.sprite.Sprite):

    """Left spikes class defying their size and position."""

    def __init__(self, cords):

        super().__init__()

        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (128, 128, 128), [(0, 0), (0, 40), (20, 20)])
        self.rect = self.image.get_rect(topleft=tuple(cords))
        self.mask = pygame.mask.from_surface(self.image)

class SpikeRight(pygame.sprite.Sprite):

    """Right spikes class defying their size and position."""

    def __init__(self, cords):

        super().__init__()

        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (128, 128, 128), [(20, 0), (20, 40), (0, 20)])
        self.rect = self.image.get_rect(topleft=tuple(cords))
        self.mask = pygame.mask.from_surface(self.image)

class SpikeTop(pygame.sprite.Sprite):

    """Top spikes class defying their size and position."""

    def __init__(self, cords):

        super().__init__()

        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (128, 128, 128), [(0, 0), (20, 20), (40, 0)])
        self.rect = self.image.get_rect(topleft=tuple(cords))
        self.mask = pygame.mask.from_surface(self.image)

class SpikeBottom(pygame.sprite.Sprite):

    """Bottom spikes class defying their size and position."""

    def __init__(self, cords):

        super().__init__()

        self.image = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (128, 128, 128), [(0, 20), (20, 0), (40, 20)])
        self.rect = self.image.get_rect(topleft=tuple(cords))
        self.mask = pygame.mask.from_surface(self.image)



class Wall(pygame.sprite.Sprite):

    """Class creating a pygame rect representing the wall."""

    def __init__(self, x, y, width, height):
        
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)




class Bird(pygame.sprite.Sprite):

    """The bird class - including appropriate bird image loading, mask calculating, jumping, physics, 
        collision with walls and spikes and sound playing."""

    def __init__(self, option):

        super().__init__()
        self.sound = pygame.mixer.Sound(os.path.join(BASE_DIR, 'Media', 'Point.mp3'))
        self.game_over = pygame.mixer.Sound(os.path.join(BASE_DIR, 'Media', 'Game_over.mp3'))

        self.option = option

        with open(os.path.join(BASE_DIR, 'Media', 'Skins.json'), 'r') as f:
            self.options = json.load(f)

        img_left = pygame.image.load(os.path.join(BASE_DIR, self.options[str(self.option)][0])).convert_alpha()
        img_right = pygame.image.load(os.path.join(BASE_DIR, self.options[str(self.option)][1])).convert_alpha()

        self.img_left = pygame.transform.smoothscale(img_left, (50, 38))
        self.img_right = pygame.transform.smoothscale(img_right, (50, 38))

        self.image = self.img_right
        self.rect = self.image.get_rect(center=(250, 350))
        self.mask = pygame.mask.from_surface(self.image)
        self.x_velocity = 5
        self.y_velocity = 0
        self.gravity = 0.5
        self.counter = 0
        self.live = True
        self.spikes_all = pygame.sprite.Group()  


    def jump(self):

        self.y_velocity = -10

    def change_image(self):

        if self.image == self.img_right:
            self.image = self.img_left
        
        else:
            self.image = self.img_right

        self.mask = pygame.mask.from_surface(self.image) 
    
    def update(self, walls, spikes):

        self.rect.x += self.x_velocity

        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity

        if self.rect.colliderect(walls[0].rect) or self.rect.colliderect(walls[1].rect):
            self.x_velocity *= -1
            self.change_image()
            self.sound.play()
            self.counter += 1

        if self.rect.colliderect(walls[2].rect):
            self.y_velocity = 0
            self.rect.y = 10

        if self.rect.colliderect(walls[3].rect):
            self.y_velocity = 0
            self.rect.bottom = 670

        self.spikes_all.empty() 

        for spike_group in spikes:
            self.spikes_all.add(spike_group.sprites())

        for spike in self.spikes_all:

            if self.rect.colliderect(spike.rect):
                offset = (spike.rect.x - self.rect.x, spike.rect.y - self.rect.y)
                if self.mask.overlap(spike.mask, offset):
                    self.live = False
                    self.game_over.play()

    def reset(self):

        self.rect.center = (250, 350)
        self.counter = 0
        self.live = True
        self.x_velocity = 5
        self.image = self.img_right
        self.spikes_all.empty()
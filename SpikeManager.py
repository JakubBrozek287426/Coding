import pygame
import random as rn
import json
import os
from SpriteClasses import SpikeLeft, SpikeRight, SpikeTop, SpikeBottom


pygame.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SpikeManager():

    """Class that handles appropriate spike generation depending on the current score. 
        It also switches the difficulty level and randomly picks the pattern every bird jump.
    """

    def __init__(self):

        with open(os.path.join(BASE_DIR, 'Media', 'Patterns.json'), 'r') as f:
            self.patterns = json.load(f)

        self.current = self.patterns['level_1']
        self.level_1_block = False
        self.level_2_block = False
        self.level_3_block = False
        self.generation_block = False
        self.counter_before = 0
        self.pattern = self.current[0]

        self.spikes_left = pygame.sprite.Group()
        self.spikes_right = pygame.sprite.Group()
        self.spikes_top = pygame.sprite.Group()
        self.spikes_bottom= pygame.sprite.Group()

        for x in self.patterns['top_bottom'][0]:
            self.spikes_top.add(SpikeTop((x, 10)))
            self.spikes_bottom.add(SpikeBottom((x, 650)))

    def change_level(self, counter):

        if counter == 0 and not self.level_1_block:

            self.current = self.patterns['level_1']
            self.level_1_block = True
            self.level_2_block = False
            self.level_3_block = False

        elif counter == 15 and not self.level_2_block:

            self.current = self.patterns['level_2']
            self.level_2_block = True
            self.level_1_block = True
            self.level_3_block = False

        elif counter == 30 and not self.level_3_block:

            self.current = self.patterns['level_3']
            self.level_3_block = True
            self.level_1_block = True
            self.level_2_block = True
    
    def pick_pattern(self, counter):
        
        if self.counter_before < counter:

            self.counter_before = counter
            self.pattern = rn.choice(self.current)
            self.generation_block = False

    def generate_spikes(self, counter):
        
        if not self.generation_block:

            if counter % 2 == 0 and counter != 0:

                self.spikes_left.empty()

                for y in self.pattern:

                    spike = SpikeRight((465, y))
                    self.spikes_right.add(spike)
                self.generation_block = True

            elif counter % 2 != 0:

                self.spikes_right.empty()

                for y in self.pattern:

                    spike = SpikeLeft((15, y))
                    self.spikes_left.add(spike)
                self.generation_block = True

    def reset(self, counter):

        self.generation_block = False
        self.spikes_right.empty()
        self.spikes_left.empty()
        self.level_1_block = False
        self.level_2_block = False
        self.level_3_block = False
        self.counter_before = 0
        self.change_level(counter)
        self.pick_pattern(counter)
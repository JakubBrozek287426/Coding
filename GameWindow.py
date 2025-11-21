import pygame
import os
from SpriteClasses import Wall, Bird
from Counter import Counter
from SpikeManager import SpikeManager
from ScoreManager import ScoreManager
from ButtonGenerator import ButtonGenerator


pygame.init()
pygame.font.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GameWindow():

    """The actual in game window. Drawing the bird, running SpikeManager methods to draw the spikes, 
        drawing the score, changing the background every 10 points.
        It has 3 states - normal (game on), static (bird in the middle waiting for SPACE pressed), game_over (showing the game over screen).
    """

    def __init__(self, screen, clock, option):

        self.screen = screen
        self.clock = clock
        self.option = option

        self.bird = Bird(self.option)
        self.counter = Counter(self.bird.counter)
        self.spike_handler = SpikeManager()
        self.archive = ScoreManager()
        self.button_generator = ButtonGenerator(self.screen)

        self.running = True

        self.highscore = 0

        self.state = "static"

        self.decision = "quit"

        self.block = False

        self.walls = [Wall(0, 0, 15, 680), 
         Wall(485, 0, 15, 680),
         Wall(0, 0, 500, 10),
         Wall(0, 670, 500, 10)]
    
    def run(self):

        while self.running:
            
            self.events = pygame.event.get()

            if self.state == "static":

                self.handle_events(self.events)
                self.draw_static()

            elif self.state == "normal":

                if self.bird.live:

                    self.block = False
                    self.handle_events(self.events)
                    self.spike_handler.change_level(self.bird.counter)
                    self.spike_handler.pick_pattern(self.bird.counter)
                    self.spike_handler.generate_spikes(self.bird.counter)
                    self.draw_normal(self.bird.counter)
                    self.bird.update(self.walls, [self.spike_handler.spikes_left, self.spike_handler.spikes_right, self.spike_handler.spikes_top, self.spike_handler.spikes_bottom])
                    self.counter.update(self.bird.counter)
                
                elif not self.bird.live and not self.block:

                    self.state = "game_over"

            elif self.state == "game_over":
                
                self.archive.add(self.bird.counter)
                self.read_highscore()
                self.handle_events(self.events)
                self.draw_game_over(self.events)

        return

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                self.decision = "quit"
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.decision = "menu"
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                if self.state == "static" and self.bird.live:
                    self.bird.jump()
                    self.state = "normal"
                elif self.state == "normal" and self.bird.live:
                    self.bird.jump()

    def draw_normal(self, counter):

        if 0 <= counter < 10:
            self.screen.fill((255,255,255))
        
        elif 10 <= counter < 20:
            self.screen.fill((255, 255, 204))

        elif 20 <= counter < 30:
            self.screen.fill((204, 255, 255))

        elif 30 <= counter < 40:
            self.screen.fill((204, 255, 204))

        else:
            self.screen.fill((221, 204, 255))


        pygame.draw.rect(self.screen, (128, 128, 128), self.walls[0].rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.walls[1].rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.walls[2].rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.walls[3].rect)
        self.spike_handler.spikes_left.draw(self.screen)
        self.spike_handler.spikes_right.draw(self.screen)
        self.spike_handler.spikes_top.draw(self.screen)
        self.spike_handler.spikes_bottom.draw(self.screen)
        self.screen.blit(self.counter.text, self.counter.text_rect)
        self.screen.blit(self.bird.image, self.bird.rect)
        pygame.display.flip()
        self.clock.tick(60)

    def draw_static(self):

        self.screen.fill((255,255,255))
        pygame.draw.rect(self.screen, (128, 128, 128), self.walls[0].rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.walls[1].rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.walls[2].rect)
        pygame.draw.rect(self.screen, (128, 128, 128), self.walls[3].rect)
        self.screen.blit(pygame.font.Font(None, 55).render("Press SPACE to start", True, (83, 83, 83)), (60, 200))
        self.screen.blit(self.bird.image, self.bird.rect)
        pygame.display.flip()
        self.clock.tick(60)

    def draw_game_over(self, events):
        
        self.screen.fill((255,255,255))
        pygame.draw.rect(self.screen, (180, 180, 180), self.walls[0].rect)
        pygame.draw.rect(self.screen, (180, 180, 180), self.walls[1].rect)
        pygame.draw.rect(self.screen, (180, 180, 180), self.walls[2].rect)
        pygame.draw.rect(self.screen, (180, 180, 180), self.walls[3].rect)
        self.screen.blit(pygame.font.Font(None, 70).render("GAME OVER", True, (83, 83, 83)), (95, 70))
        self.screen.blit(pygame.font.Font(None, 45).render("Your score was:", True, (83, 83, 83)), (130, 140))
        self.screen.blit(pygame.font.Font(None, 90).render(f"{self.bird.counter:03}", True, (83, 83, 83)), (195, 190))
        self.screen.blit(pygame.font.Font(None, 45).render("Highscore:", True, (83, 83, 83)), (170, 280))
        self.screen.blit(pygame.font.Font(None, 90).render(f"{self.highscore:03}", True, (83, 83, 83)), (195, 330))   
        self.button_generator.generate_button(80, 430, 340, 100, (180, 180, 180), (140, 140, 140), "PLAY AGAIN", (140, 465), (80, 80, 80), (80, 80, 80), events, self.restart)
        self.button_generator.generate_button(80, 534, 340, 100, (180, 180, 180), (140, 140, 140), "MAIN MENU", (145, 569), (80, 80, 80), (80, 80, 80), events, self.back_to_menu)
        pygame.display.flip()
        self.clock.tick(60)

    def restart(self):
        self.state = "static"
        self.block = True
        self.bird.reset()
        self.spike_handler.reset(self.bird.counter)

    def read_highscore(self):

        with open(os.path.join(BASE_DIR, 'Media', 'scores.txt'), 'r') as f:

            line = f.readline().strip()
            if line.isdigit():
                self.highscore = int(line)
            else:
                self.highscore = 0

    def back_to_menu(self):
        self.decision = "menu"
        self.running = False
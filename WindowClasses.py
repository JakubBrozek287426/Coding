import pygame
import os
from ButtonGenerator import ButtonGenerator, BirdButtonGenerator
from ScoreManager import ScoreManager


pygame.init()
pygame.font.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class AuthorWindow():

    """Window with the information about the author of the game."""

    def __init__(self, screen, clock):

        self.screen = screen
        self.clock = clock
        self.running = True
        self.decision = "quit"
        self.button_generator = ButtonGenerator(self.screen)
        self.font_big = pygame.font.Font(None, 55)
        self.font_small = pygame.font.Font(None, 35)
        self.font_huge = pygame.font.Font(None, 80)

    def run(self):

        while self.running:
             
            self.events = pygame.event.get()
            self.handle_events(self.events)
            self.draw(self.events)

        return

    def draw(self, events):

            self.screen.fill((255,255,255))

            self.screen.blit(self.font_huge.render("About Author", True, (83, 83, 83)), (67, 60))
            self.screen.blit(self.font_small.render("I am Jakub Brozek and this game", True, (83, 83, 83)), (25, 150))
            self.screen.blit(self.font_small.render("is a result of a 'Game in a week' project.", True, (83, 83, 83)), (25, 180))
            self.screen.blit(self.font_small.render("Bird graphics are my own. Enjoy!", True, (83, 83, 83)), (25, 210))

            self.button_generator.generate_button(50, 550, 400, 100, (180, 180, 180), (140, 140, 140), "MAIN MENU", (147, 588), (80, 80, 80), (80, 80, 80), events, self.go_to_menu)

            pygame.display.flip()
            self.clock.tick(60)
    
    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                self.decision = "quit"
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.decision = "menu"
                self.running = False

    def go_to_menu(self):
        self.decision = "menu"
        self.running = False



class RulesWindow():
    
    """Window with the rules of the game."""

    def __init__(self, screen, clock):

        self.screen = screen
        self.clock = clock
        self.running = True
        self.decision = "quit"
        self.button_generator = ButtonGenerator(self.screen)
        self.font_small = pygame.font.Font(None, 35)
        self.font_huge = pygame.font.Font(None, 80)

    def run(self):

        while self.running:
            
            self.events = pygame.event.get()
            self.handle_events(self.events)
            self.draw(self.events)

        return
    
    def draw(self, events):

            self.screen.fill((255,255,255))

            self.screen.blit(self.font_huge.render("Game Rules", True, (83, 83, 83)), (80, 40))
            self.screen.blit(self.font_small.render("- Press space to make the bird fly up", True, (83, 83, 83)), (20, 150))
            self.screen.blit(self.font_small.render("- Try to avoid the spikes", True, (83, 83, 83)), (20, 200))
            self.screen.blit(self.font_small.render("- You score a point after hitting the wall", True, (83, 83, 83)), (20, 250))
            self.screen.blit(self.font_small.render("- Score as many points as you can", True, (83, 83, 83)), (20, 300))

            self.button_generator.generate_button(50, 550, 400, 100, (180, 180, 180), (140, 140, 140), "MAIN MENU", (147, 588), (80, 80, 80), (80, 80, 80), events, self.go_to_menu)

            pygame.display.flip()
            self.clock.tick(60)
        
    
    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                self.decision = "quit"
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.decision = "menu"
                self.running = False

    def go_to_menu(self):
        self.decision = "menu"
        self.running = False



class HighScoreWindow():

    """Window with the Highscore."""

    def __init__(self, screen, clock):

        self.screen = screen
        self.clock = clock
        self.running = True
        self.decision = "quit"
        self.font_big = pygame.font.Font(None, 55)
        self.font_small = pygame.font.Font(None, 50)
        self.font_huge = pygame.font.Font(None, 140)
        self.button_generator = ButtonGenerator(self.screen)
        self.reset_score = ScoreManager()
        self.score = 0

    def run(self):

        with open(os.path.join(BASE_DIR, 'Media', 'scores.txt'), 'r') as f:

            line = f.readline().strip()
            if line.isdigit():
                self.score = int(line)
            else:
                self.score = 0
        
        while self.running:
            
            self.events = pygame.event.get()
            self.handle_events(self.events)
            self.draw(self.events)
        
        return
    
    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                self.decision = "quit"
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.decision = "menu"
                self.running = False

    def draw(self, events):

            self.screen.fill((255,255,255))

            self.screen.blit(self.font_big.render("Your highscore is:", True, (83, 83, 83)), (75, 100))
            self.screen.blit(self.font_huge.render(f"{self.score:03}", True, (83, 83, 83)), (160, 200))

            self.button_generator.generate_button(50, 446, 400, 100, (180, 180, 180), (140, 140, 140), "RESET", (192, 484), (80, 80, 80), (80, 80, 80), events, self.reset)
            self.button_generator.generate_button(50, 550, 400, 100, (180, 180, 180), (140, 140, 140), "MAIN MENU", (147, 588), (80, 80, 80), (80, 80, 80), events, self.go_to_menu)

            pygame.display.flip()
            self.clock.tick(60)

    def go_to_menu(self):
        self.decision = "menu"
        self.running = False

    def reset(self):
        self.reset_score.reset()
        with open(os.path.join(BASE_DIR, 'Media', 'scores.txt'), 'r') as f:

            line = f.readline().strip()
            if line.isdigit():
                self.score = int(line)
            else:
                self.score = 0

    

class SettingsWindow():

    """Window with the possibility to pick a skin using for example buttons created with BirdButtonGenerator."""

    def __init__(self, screen, clock, option):

        self.screen = screen
        self.clock = clock
        self.running = True
        self.decision = "quit"
        self.font_big = pygame.font.Font(None, 55)
        self.font_small = pygame.font.Font(None, 50)
        self.font_huge = pygame.font.Font(None, 70)
        self.button_generator = ButtonGenerator(self.screen)
        self.bird_1_button = BirdButtonGenerator(self.screen, os.path.join(BASE_DIR, 'Media', 'Custom1_left.png'), os.path.join(BASE_DIR, 'Media', 'Custom1_left_gray.png'), 0, 1)
        self.bird_2_button = BirdButtonGenerator(self.screen, os.path.join(BASE_DIR, 'Media', 'Custom2_left.png'), os.path.join(BASE_DIR, 'Media', 'Custom2_left_gray.png'), 10, 2)
        self.bird_3_button = BirdButtonGenerator(self.screen, os.path.join(BASE_DIR, 'Media', 'Custom3_left.png'), os.path.join(BASE_DIR, 'Media', 'Custom3_left_gray.png'), 20, 3)
        self.bird_4_button = BirdButtonGenerator(self.screen, os.path.join(BASE_DIR, 'Media', 'Custom4_left.png'), os.path.join(BASE_DIR, 'Media', 'Custom4_left_gray.png'), 30, 4)
        self.bird_5_button = BirdButtonGenerator(self.screen, os.path.join(BASE_DIR, 'Media', 'Custom5_left.png'), os.path.join(BASE_DIR, 'Media', 'Custom5_left_gray.png'), 40, 5)
        self.bird_6_button = BirdButtonGenerator(self.screen, os.path.join(BASE_DIR, 'Media', 'Custom6_left.png'), os.path.join(BASE_DIR, 'Media', 'Custom6_left_gray.png'), 50, 6)
        self.bird_7_button = BirdButtonGenerator(self.screen, os.path.join(BASE_DIR, 'Media', 'Custom7_left.png'), os.path.join(BASE_DIR, 'Media', 'Custom7_left_gray.png'), 60, 7)

        self.option = option

    def run(self):

        while self.running:

            self.events = pygame.event.get()
            self.handle_events(self.events)
            self.draw(self.events)
        return
    
    def draw(self, events):

        self.screen.fill((255,255,255))

        self.screen.blit(self.font_huge.render("Choose your bird", True, (83, 83, 83)), (40, 40))

        self.bird_1_button.generate_button(60, 220, self.option, self.events, self.change_bird)
        self.bird_2_button.generate_button(200, 220, self.option, self.events, self.change_bird)
        self.bird_3_button.generate_button(340, 220, self.option, self.events, self.change_bird)
        self.bird_4_button.generate_button(60, 320, self.option, self.events, self.change_bird)
        self.bird_5_button.generate_button(200, 320, self.option, self.events, self.change_bird)
        self.bird_6_button.generate_button(340, 320, self.option, self.events, self.change_bird)
        self.bird_7_button.generate_button(60, 420, self.option, self.events, self.change_bird)

        self.button_generator.generate_button(50, 550, 400, 100, (180, 180, 180), (140, 140, 140), "MAIN MENU", (147, 588), (80, 80, 80), (80, 80, 80), events, self.go_to_menu)

        pygame.display.flip()
        self.clock.tick(60)

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                self.decision = "quit"
                self.running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.decision = "menu"
                self.running = False

    def go_to_menu(self):
        self.decision = "menu"
        self.running = False

    def change_bird(self, bird):
        self.option = bird
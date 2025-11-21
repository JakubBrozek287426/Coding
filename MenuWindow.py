import pygame
import os
from ButtonGenerator import ButtonGenerator


pygame.init()
pygame.font.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MenuWindow():

    """Menu window class. Handles drawing the buttons in the main menu, 
        all the decisions after pressing particular button that are then sent to WindowManager.
        It is the first window after running the game.
    """

    def __init__(self, screen, clock):

            self.screen = screen
            self.clock = clock
            self.running = True
            self.decision = "menu"
            self.font_big = pygame.font.Font(None, 55)
            self.font_small = pygame.font.Font(None, 50)
            self.score = 0
            self.button_generator = ButtonGenerator(self.screen)

            pick_bird_image = pygame.image.load(os.path.join(BASE_DIR, 'Media', 'Pick_bird.png')).convert_alpha()
            self.pick_bird_image = pygame.transform.smoothscale(pick_bird_image, (50, 40))
            self.pick_bird_rect = self.pick_bird_image.get_rect(topleft=(440, 630))

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
    
    def draw(self, events):

        self.screen.fill((255,255,255))
        self.screen.blit(self.font_big.render("Don't Touch The Spikes", True, (83, 83, 83)), (30, 80))

        self.button_generator.generate_button(50, 200, 400, 100, (180, 180, 180), (140, 140, 140), "START", (192, 238), (80, 80, 80), (80, 80, 80), events, self.start_game)
        self.button_generator.generate_button(50, 304, 198, 100, (180, 180, 180), (140, 140, 140), "AUTHOR", (70, 338), (80, 80, 80), (80, 80, 80), events, self.go_to_author)
        self.button_generator.generate_button(252, 304, 198, 100, (180, 180, 180), (140, 140, 140), "RULES", (290, 338), (80, 80, 80), (80, 80, 80), events, self.go_to_rules)
        self.button_generator.generate_button(50, 408, 400, 100, (180, 180, 180), (140, 140, 140), f"HIGHSCORE: {self.score:03}", (100, 442), (80, 80, 80), (80, 80, 80), events, self.go_to_highscore)
        self.button_generator.generate_button(50, 512, 400, 100, (180, 180, 180), (140, 140, 140), "EXIT", (205, 548), (80, 80, 80), (80, 80, 80), events, self.exit_game)

        self.screen.blit(self.pick_bird_image, self.pick_bird_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def handle_events(self, events):
          
        for event in events:

            mouse = pygame.mouse.get_pos()

            if event.type == pygame.QUIT: 
                self.exit_game()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit_game()
            
            if  440 < mouse[0] < 490 and 630 < mouse[1] < 670 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.go_to_settings()


    def start_game(self):
        self.decision = "play"
        self.running = False

    def exit_game(self):
        self.decision = "quit"
        self.running = False

    def go_to_highscore(self):
        self.decision = "highscore"
        self.running = False

    def go_to_rules(self):
        self.decision = "rules"
        self.running = False

    def go_to_author(self):
        self.decision = "author"
        self.running = False
    
    def go_to_settings(self):
        self.decision = "settings"
        self.running = False
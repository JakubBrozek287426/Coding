import pygame
import os


pygame.init()
pygame.font.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ButtonGenerator():

    """Class that creates a button with text in it. The generate_button method takes multiple arguments such as button position and size.
        It makes a clickable button (tracking a mouse position from particular windows pygame events), 
        the button can chage its color when hovered.
    """

    def __init__(self, screen):

        self.screen = screen
        self.font_big = pygame.font.Font(None, 55)
        self.font_small = pygame.font.Font(None, 50)

    def generate_button(self, x, y, width, height, inactive_color, active_color, text, text_pos, inactive_text_color, active_text_color, events, action=None, arg=None):
        
        mouse = pygame.mouse.get_pos()
        clicked = False
        hovered = x < mouse[0] < x + width and y < mouse[1] < y + height

        if hovered:
            pygame.draw.rect(self.screen, active_color, (x, y, width, height))
            self.screen.blit(self.font_small.render(text, True, active_text_color), text_pos)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked = True
        else:
            pygame.draw.rect(self.screen, inactive_color, (x, y, width, height))
            self.screen.blit(self.font_small.render(text, True, inactive_text_color), text_pos)

        if clicked and action:
            if arg:
                action(arg)
            else:
                action()


class BirdButtonGenerator():
    
    """Class made just to simplify the SettingsWindow class. It loads particular bird images, creates clickable bird button that turns more
        colorful when hovered. When the bird is currently active it is in color until changed. It also handles showing on what condition 
        the bird can be unlocked while drawing the mystery bird icon and making the button unclickable.
    """

    def __init__(self, screen, img_n, img_g, threshold, argument):

        self.screen = screen
        self.threshold = threshold
        self.argument = argument
        self.font_big = pygame.font.Font(None, 55)
        self.font_small = pygame.font.Font(None, 50)
        self.img_normal_t = pygame.transform.smoothscale(pygame.image.load(img_n).convert_alpha(), (79, 60))
        self.img_gray_t = pygame.transform.smoothscale(pygame.image.load(img_g).convert_alpha(), (79, 60))
        self.img_mystery_t = pygame.transform.smoothscale(pygame.image.load(os.path.join(BASE_DIR, 'Media', 'Mystery.png')).convert_alpha(), (79, 60))

        with open(os.path.join(BASE_DIR, 'Media', 'scores.txt'), 'r') as f:

            line = f.readline().strip()
            if line.isdigit():
                self.highscore = int(line)
            else:
                self.highscore = 0

    def generate_button(self, x, y, current_option, events, action):

        mouse = pygame.mouse.get_pos()
        clicked = False
        hovered = x < mouse[0] < x + 79 and y < mouse[1] < y + 60

        img_rect = self.img_normal_t.get_rect(topleft=(x, y))
        if self.threshold == 0:
            text = 'Base bird'
            pos = (170, 500)
        else:
            text = f"For {self.threshold:03} points scored"
            pos = (80, 500)

        if self.highscore == 0:
            action(1)

        if self.highscore < self.threshold:
            self.screen.blit(self.img_mystery_t, img_rect)
            if hovered:
                self.screen.blit(self.font_small.render(f"Score {self.threshold} to unlock", True, (83, 83, 83)), (100, 500))
            return

        elif current_option == self.argument:
            self.screen.blit(self.img_normal_t, img_rect)

            if hovered:

                self.screen.blit(self.font_small.render(text, True, (83, 83, 83)), pos)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        clicked = True
    
        else:
            if hovered:
                self.screen.blit(self.img_normal_t, img_rect)
                self.screen.blit(self.font_small.render(text, True, (83, 83, 83)), pos)
                for event in events:

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        clicked = True
            else:
                self.screen.blit(self.img_gray_t, img_rect)

        if clicked and action:
            action(self.argument)
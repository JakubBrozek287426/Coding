import pygame


pygame.init()
pygame.font.init()

class Counter():

    """Class setting the counter in the right place and updating it every point."""

    def __init__(self, counter):

        self.font = pygame.font.Font(None, 250)
        self.update(counter)
    
    def update(self, counter):

        self.text = self.font.render(str(counter), True, (83, 83, 83)).convert_alpha()
        self.text.set_alpha(128)
        self.text_rect = self.text.get_rect(center=(250,340))
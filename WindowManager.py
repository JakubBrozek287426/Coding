import pygame
from GameWindow import GameWindow
from MenuWindow import MenuWindow
from WindowClasses import AuthorWindow, RulesWindow, HighScoreWindow, SettingsWindow


pygame.init()

class WindowManager():

    """Class which manages all the windows. Displaying MenuWindow at first 
        and than opening appropriate windows depending on the decision from currently active window.
        For example - when 'Main Menu' button is pressed current window is closed and WindowManager opens the MenuWindow.
        It is where the game starts.
    """

    def __init__(self):
        
        self.screen = pygame.display.set_mode((500,680))
        self.clock = pygame.time.Clock()
        self.mode = "menu"
        self.running = True
        self.option = 1
        
    def run(self):
        
        while self.running:
            
            if self.mode == "game":
                self.game = GameWindow(self.screen, self.clock, self.option)
                self.game.run()
                if self.game.decision == "quit":
                    break
                elif self.game.decision == "menu": 
                    self.mode = "menu"
            
            if self.mode == "menu":
                self.menu = MenuWindow(self.screen, self.clock)
                self.menu.run()
                if self.menu.decision == "quit":
                    break
                elif self.menu.decision == "play":
                    self.mode = "game"
                elif self.menu.decision == "highscore":
                    self.mode = "highscore"
                elif self.menu.decision == "rules":
                    self.mode = "rules"
                elif self.menu.decision == "author":
                    self.mode = "author"
                elif self.menu.decision == "settings":
                    self.mode = "settings"

            if self.mode == "highscore":
                self.highscore = HighScoreWindow(self.screen, self.clock)
                self.highscore.run()
                if self.highscore.decision == "quit":
                    break
                elif self.highscore.decision == "menu":
                    self.mode = "menu"

            if self.mode == "rules":
                self.rules = RulesWindow(self.screen, self.clock)
                self.rules.run()
                if self.rules.decision == "quit":
                    break
                elif self.rules.decision == "menu":
                    self.mode = "menu"

            if self.mode == "author":
                self.author = AuthorWindow(self.screen, self.clock)
                self.author.run()
                if self.author.decision == "quit":
                    break
                elif self.author.decision == "menu":
                    self.mode = "menu"

            if self.mode == "settings":
                self.settings = SettingsWindow(self.screen, self.clock, self.option)
                self.settings.run()
                self.option = self.settings.option
                if self.settings.decision == "quit":
                    break
                elif self.settings.decision == "menu":
                    self.mode = "menu"

        pygame.quit()

window = WindowManager()
window.run()
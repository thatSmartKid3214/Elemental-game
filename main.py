import pygame
import sys
import scripts
import os
from scripts.Engine import JSON_Handler

pygame.init()

W = 640
H = 360
DISPLAY_W = 320
DISPLAY_H = 180


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
        self.display = pygame.Surface((DISPLAY_W, DISPLAY_H))
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_dir = os.getcwd()
        self.assets = scripts.Assets(self.current_dir)
        
        self.GM = scripts.Game_Manager(self)
    
    def close(self):
        self.running = False
    
    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.GM.run()
        
        pygame.quit()
        sys.exit()

Game().run()
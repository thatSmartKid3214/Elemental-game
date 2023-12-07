import pygame
import scripts.Engine as E


class Trapdoor:
    def __init__(self, images, pos):
        self.pos = pos
        self.images = images
        self.img = images[0]
        self.rect = self.img.get_rect(topleft=pos)
        self.open_timer = E.Timer(0.2, self.open)
        self.close_timer = E.Timer(1.5, self.close)
        self.opened = False
    
    def draw(self, surf, scroll):
        if self.opened:
            self.img = self.images[1]
        else:
            self.img = self.images[0]
        
        surf.blit(self.img, (self.rect.x-scroll[0], self.rect.y-6-scroll[1]))
    
    def open(self):
        self.opened = True
        self.close_timer.set()
    
    def close(self):
        self.opened = False
    
    def update(self):
        self.open_timer.update()
        self.close_timer.update()



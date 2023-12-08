import pygame
import scripts.Engine as E


class Door:
    def __init__(self, images, pos, type):
        self.pos = pos
        self.type = type
        if self.type == "wood":
            self.pos[0] += 6
        if self.type == "gold":
            self.pos[0] += 3
        self.images = images
        self.img = images[0]
        self.rect = self.img.get_rect(topleft=self.pos)
        self.closed = True
        self.locked = False
        self.flip = False
        
        if self.type == "wood":
            self.rect.width = 4
        
        if self.type == "gold":
            self.locked = True
            self.rect.width = 10
    
    def draw(self, surf, scroll):
        x = 7
        if self.type == "gold":
            x = 4
        if not self.closed:
            self.img = self.images[1]
        else:
            self.img = self.images[0]
            self.flip = False
        
        if self.type == "wood":
            if not self.flip and not self.closed:
                x = 12
            if self.flip and not self.closed:
                x = 14
        if self.type == "gold":
            if not self.flip and not self.closed:
                x = 10
            if self.flip and not self.closed:
                x = 12
                
            surf.blit(self.images[2], (self.rect.x-13-scroll[0], self.rect.centery-8-scroll[1]))
            surf.blit(self.images[2], (self.rect.right-3-scroll[0], self.rect.centery-8-scroll[1]))
            
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.rect.x-x-scroll[0], self.rect.y-scroll[1]))




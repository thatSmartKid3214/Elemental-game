import pygame
import math
from scripts.Engine import blit_center

class Particle:
    def __init__(self, pos: list, vel: list, rotation: int, size: int, color: list or tuple, alpha: int, acceleration: int =[0, 0], gravity=0, deterioration=0.1, fade = 0, outline: int = 0, image: pygame.Surface = None, shape="square"):
        self.pos = pos
        self.vel = vel
        self.size = size
        self.color = color
        self.shape = shape
        self.alpha = alpha
        self.image = pygame.Surface((size, size)) 
        self.image.set_colorkey((0, 0, 0))
        
        if shape == "image":
            self.image = image
            #self.size = self.image.get_width()
        
        self.acceleration = acceleration
        self.gravity = gravity
        self.deterioration = deterioration
        self.fade = fade
        self.angle = 0
        self.rotation = rotation
        self.outline = outline
        self.alive = True
    
    def draw(self, surf, scroll):
        if self.shape == "square":
            pygame.draw.rect(self.image, self.color, (0, 0, self.size, self.size), self.outline)
        if self.shape == "circle":
            self.size = max(2, self.size)
            pygame.draw.circle(self.image, self.color, (self.size/2, self.size/2), self.size/2, self.outline)
        if self.shape == "triangle":
            pos = [self.size/2, self.size/2]
            points = [[pos[0], pos[1]-self.size/2], [pos[0]-self.size/2, pos[1]+self.size/2], [pos[0]+self.size/2, pos[1]+self.size/2]]
            pygame.draw.polygon(self.image, self.color, points)

        blit_center(surf, pygame.transform.rotate(self.image, self.angle), (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))
        
    def update(self):
        if self.size <= 0:
            self.alive = False
        if self.alpha <= 0:
            self.alive = False
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.size -= self.deterioration
        self.alpha -= self.fade
        self.angle += self.rotation
        if self.angle >= 360:
            self.angle = 0
        
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.image.set_alpha(self.alpha)
        
        self.vel[1] += self.gravity
        
        if self.vel[0] > 0:
            self.vel[0] = max(0, self.vel[0]-self.acceleration[0])
        if self.vel[0] < 0:
            self.vel[0] = min(0, self.vel[0]+self.acceleration[0])
        
        if self.vel[1] > 0:
            self.vel[1] = max(0, self.vel[1]-self.acceleration[1])
        if self.vel[1] < 0:
            self.vel[1] = min(0, self.vel[1]+self.acceleration[1])


class ExplosionParticle(Particle):
    def __init__(self, pos: list, vel: list, rotation: int, size: int, color: list or tuple, alpha: int, acceleration: int =[0, 0], gravity=0, deterioration=0.1, fade = 0,  expand = 0, image: pygame.Surface = None, shape="square"):
        super().__init__(pos, vel, rotation, size, color, alpha, acceleration, gravity, deterioration, fade, image, shape)
        self.expand = expand
    
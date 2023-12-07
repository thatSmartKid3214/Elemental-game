
import pygame
import scripts.Engine as E


class Spike:
    def __init__(self, img: pygame.Surface, pos, spike_id, type="normal"):
        self.pos = pos
        self.spike_id = spike_id
        self.img = img
        self.rect = img.get_rect(topleft=pos)
        self.detection_rect = img.get_rect(topleft=pos)
        x, y = 0, 0
        if spike_id == 81:
            y = img.get_height()
        if spike_id == 82:
            y = -img.get_height()
        if spike_id == 83:
            x = img.get_width()
        if spike_id == 84:
            x = -img.get_width()
        
        self.detection_rect.x -= x
        self.detection_rect.y -= y
        self.type = type
        self.recede_timer = E.Timer(1)
        self.move_timer = E.Timer(0.2, self.recede_timer.set)
        self.active = False
        
        if self.type == "hidden":
            if spike_id == 81:
                self.rect.height = img.get_height()-8
                self.detection_rect.y += 16
                self.rect.y += 16
            if spike_id == 82:
                self.rect.height = img.get_height()-8
                self.detection_rect.y -= 16
                self.rect.y -= 8
            if spike_id == 83:
                self.rect.width = img.get_width()-8
                self.detection_rect.x += 16
                self.rect.x += 16
            if spike_id == 84:
                self.rect.width = img.get_width()-8
                self.detection_rect.x -= 16
                self.rect.x -= 8
    
    def draw(self, surf, scroll):
        pos = (self.rect.x-scroll[0], self.rect.y-scroll[1])
        
        if self.type == "hidden":
            if self.spike_id == 81:
                pos = (self.rect.x-scroll[0], self.rect.y-6-scroll[1])
            if self.spike_id == 82:
                pos = (self.rect.x-scroll[0], self.rect.y-2-scroll[1])
            if self.spike_id == 83:
                pos = (self.rect.x-6-scroll[0], self.rect.y-scroll[1])
            if self.spike_id == 84:
                pos = (self.rect.x-2-scroll[0], self.rect.y-scroll[1])
        
        surf.blit(self.img, pos)
        #pygame.draw.rect(surf, (255, 0, 0), (self.rect.x-scroll[0], self.rect.y-scroll[1], self.rect.width, self.rect.height), 1)
        #pygame.draw.rect(surf, (255, 255, 0), (self.detection_rect.x-scroll[0], self.detection_rect.y-scroll[1], self.detection_rect.width, self.detection_rect.height), 1)
    
    def update(self):
        if self.active:
            self.move_timer.update()
            
            if self.spike_id == 81 and self.move_timer.timed_out():
                self.rect.y -= 2
                
                if self.rect.y < self.pos[1]+6:
                    self.rect.y = self.pos[1]+6
                
                self.recede_timer.update()
            
                if self.recede_timer.timed_out():
                    self.active = False
            
            if self.spike_id == 82 and self.move_timer.timed_out():
                self.rect.y += 2
                
                if self.rect.y > self.pos[1]+2:
                    self.rect.y = self.pos[1]+2
                
                self.recede_timer.update()
            
                if self.recede_timer.timed_out():
                    self.active = False
            
            if self.spike_id == 83 and self.move_timer.timed_out():
                self.rect.x -= 2
                
                if self.rect.x < self.pos[0]+6:
                    self.rect.x = self.pos[0]+6
                
                self.recede_timer.update()
            
                if self.recede_timer.timed_out():
                    self.active = False
            
            if self.spike_id == 84 and self.move_timer.timed_out():
                self.rect.x += 2
                
                if self.rect.x > self.pos[0]+2:
                    self.rect.x = self.pos[0]+2
                
                self.recede_timer.update()
            
                if self.recede_timer.timed_out():
                    self.active = False
        
        if self.active == False and self.type == "hidden":
            if self.spike_id == 81:
                self.rect.y += 2
                if self.rect.y > self.pos[1] + 16:
                    self.rect.y = self.pos[1] + 16
            if self.spike_id == 82:
                self.rect.y -= 2
                if self.rect.y < self.pos[1] - 8:
                    self.rect.y = self.pos[1] - 8
            if self.spike_id == 83:
                self.rect.x += 2
                if self.rect.x > self.pos[0]+16:
                    self.rect.x = self.pos[0]+16
            if self.spike_id == 84:
                self.rect.x -= 2
                if self.rect.x < self.pos[0]-8:
                    self.rect.x = self.pos[0]-8
            
            



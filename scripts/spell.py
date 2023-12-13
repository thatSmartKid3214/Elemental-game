
import pygame
import random
import math
import scripts.Engine as E
from scripts.particle import Particle

colors = {}


class Spell:
    def __init__(self, type, name, description, mastery, dmg, cast_cooldown, duration=0):
        self.type = type
        self.name = name
        self.description = description
        self.mastery = mastery
        self.dmg = dmg
        self.cast_cooldown = E.Timer(cast_cooldown)
        self.duration = E.Timer(duration)
    
    
class Spellcast:
    def __init__(self, gm, spell: Spell, caster):
        self.gm = gm
        self.caster = caster
        self.spell = spell
        self.spell.duration.set()
        self.animation = None
        if self.spell.name in self.gm.assets.spells[self.spell.type]:
            self.animation = E.Animation()
            self.animation.load_anim(self.gm.assets.spells[self.spell.type][self.spell.name][1], "anim", self.gm.assets.spells[self.spell.type][self.spell.name][0])
            if self.spell.name in ["flame_slash", "flame_thrower"]:
                self.animation.set_loop(False)
            
        self.colliders = []
        self.flip_x = False
        self.flip_y = False
        self.angle = False
        self.active = True
    
    def cast(self, pos, vel, angle=0):
        if self.spell.type in ["fire", "water", "lightning"] and self.spell.name == "attack":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 12, 12), vel])
        if self.spell.name == "fireball":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 32, 18), vel])
        if self.spell.name == "flame_slash":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 12, 32), vel])
        if self.spell.name == "flame_thrower":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 56, 32), [0, 0]])
        
        if vel[0] < 0:
            self.flip_x = True
        if vel[1] < 0:
            self.flip_y = True
        
        self.angle = angle
    
    def draw(self, surf, scroll):
        if self.active:
            if self.animation != None:
                
                frame_loop = None
                if self.spell.name == "flame_thrower":
                    
                    if not self.spell.duration.timed_out() and self.animation.frame_count >= 35:
                        frame_loop = [35, 49]
                
                img, frame = self.animation.animate("anim", True, True, loop_between= frame_loop)

                if self.spell.name == "attack":
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-2-scroll[0], self.colliders[0][0].y-2-scroll[1]))
                if self.spell.name == "fireball":
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-scroll[0], self.colliders[0][0].y-7-scroll[1]))
                if self.spell.name == "flame_slash":
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-2-scroll[0], self.colliders[0][0].y-scroll[1]))
                if self.spell.name == "flame_thrower":
                    if self.flip_x:
                        surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-8-scroll[0], self.colliders[0][0].y-scroll[1]))
                    else:
                        surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-scroll[0], self.colliders[0][0].y-scroll[1]))
                    
                
                if self.gm.debug_render:
                    for rect, _ in self.colliders:
                        pygame.draw.rect(surf, (120, 0,175), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
                
            else:
                pass
        
            

    def update(self):
        if self.active:
            if self.spell.type in ["fire", "water", "lightning"] and self.spell.name ==  "attack":
                self.colliders[0][0].x += self.colliders[0][1][0]
                self.colliders[0][0].y += self.colliders[0][1][1]
            if self.spell.name in ["fireball", "flame_slash"]:
                self.colliders[0][0].x += self.colliders[0][1][0]
                self.colliders[0][0].y += self.colliders[0][1][1]
            
            if self.spell.name == "flame_thrower":
                self.flip_x = self.gm.player.flip
                
                self.colliders[0][0].topleft = [self.gm.player.rect.right+5, self.gm.player.rect.y]
                
                if self.flip_x:
                    self.colliders[0][0].topleft = [self.gm.player.rect.x-5-self.colliders[0][0].width, self.gm.player.rect.y]
                    
                                    
                if self.animation.frame_count+1 >= len(self.animation.frames["anim"]):
                    self.active = False
        
        if self.spell.name in ["attack", "fireball", "flame_slash"]:
            for rect, _ in self.colliders:
                for collider in self.gm.colliders["tiles"]:
                    if rect.colliderect(collider):
                        self.active = False
        
        self.spell.duration.update()
        


class SpellManager:
    def __init__(self, gm):
        self.gm = gm
        self.spells = []
    
    def handle_player_casting(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                spell = Spellcast(self.gm, self.gm.player.default_spell, "player")
                vel = [7, 0]
                pos = [self.gm.player.rect.right + 3, self.gm.player.rect.centery - 6]
                if self.gm.player.flip:
                    vel = [-7, 0]
                    pos = [self.gm.player.rect.left - 15, self.gm.player.rect.centery - 6]
                spell.cast(pos, vel)
                self.spells.append(spell)
        
        if event.type == pygame.KEYDOWN:
            if event.key in self.gm.player.spells[self.gm.player.mode]:
                spell = Spellcast(self.gm, self.gm.player.spells[self.gm.player.mode][event.key], "player")
                
                pos = [0, 0]
                vel = [0, 0]
                
                if self.gm.player.flip:
                    if spell.spell.name == "fireball":
                        pos = [self.gm.player.rect.left - 37, self.gm.player.rect.y+9]
                        vel = [-8, 0]
                    if spell.spell.name == "flame_slash":
                        pos = [self.gm.player.rect.left - 7, self.gm.player.rect.y]
                        vel = [-8, 0]
                else:
                    if spell.spell.name == "fireball":
                        pos = [self.gm.player.rect.right + 5, self.gm.player.rect.y+9]
                        vel = [8, 0]
                    if spell.spell.name == "flame_slash":
                        pos = [self.gm.player.rect.right + 5, self.gm.player.rect.y]
                        vel = [8, 0]
                        
                spell.cast(pos, vel)
                self.spells.append(spell) 
    
    def update(self):
        for i, spell in sorted(enumerate(self.spells), reverse=True):
            spell.update()
            spell.draw(self.gm.game.display, self.gm.camera.scroll)
            
            if spell.active == False:
                self.spells.pop(i)



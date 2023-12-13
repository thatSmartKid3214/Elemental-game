
import pygame
import random
import math
import scripts.Engine as E
from scripts.particle import Particle

vec2 = pygame.Vector2

colors = {}


class Spell:
    def __init__(self, type, name, description, mastery, dmg, cast_cooldown, count = 0, duration=0):
        self.type = type
        self.name = name
        self.description = description
        self.mastery = mastery
        self.dmg = dmg
        self.count = count
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
        self.exploded = False
        self.moving = False
        
        self.explosion_hitboxes = []
        
        self.attack_time = 0
        
        self.active = self.spell.cast_cooldown.timed_out()
    
    def cast(self, pos, vel, angle=0):
        if self.spell.type in ["fire", "water", "lightning"] and self.spell.name == "attack":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 12, 12), vel])
        if self.spell.name == "fireball":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 32, 18), vel])
        if self.spell.name == "flame_slash":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 12, 32), vel])
        if self.spell.name == "flame_thrower":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 56, 32), [0, 0]])
        if self.spell.name == "splash":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 32, 32), vel])
        if self.spell.name == "water_arrow":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 36, 16), vel])
        if self.spell.name == "drown":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 61, 64), vel])
        if self.spell.name == "ice_wall":
            self.colliders.append([pygame.FRect(pos[0], pos[1], 10, 48), vel])
        if self.spell.name == "fire rain":
            
            r = [pos[0]-32, pos[0]+32, pos[1]-80, pos[1]-64]
            
            for i in range(8):
                p = [random.randint(r[0], r[1]), random.randint(r[2], r[3])]
                angle = math.atan2(p[1]-pos[1], pos[0]-p[0])
                t = [pygame.FRect(p[0], p[1], 8, 8), [math.cos(angle)*4*random.uniform(0.8, 1), math.sin(-angle)*4*random.uniform(0.8, 1)]]
                self.colliders.append(t)
        if self.spell.name == "flame bombs":
            for i in range(5):
                v = [0, 0]
                if vel[0] < 0:
                    v[0] = random.uniform(-1.5, -0.4) 
                if vel[0] > 0:
                    v[0] = random.uniform(0.4, 1.5) 
                
                if vel[1] < 0:
                    v[1] = random.uniform(-0.3, -0.1) * random.uniform(0.5, 0.6)
                    vel[1] = random.choice([-1, 1])
                if vel[1] > 0:
                    v[1] = random.uniform(0.1, 0.3) * random.uniform(0.5, 0.6)
                    vel[1] = random.choice([-1, 1])
                
                c = [pygame.FRect(pos[0], pos[1]+random.randint(-8, 8), 4, 4), v]
                self.colliders.append(c)
        
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
                
                if self.spell.name == "drown":
                    if not self.spell.duration.timed_out() and self.animation.frame_count >= 20:
                        frame_loop = [20, 23]
                
                if self.spell.name == "ice_wall":
                    if not self.spell.duration.timed_out() and self.animation.frame_count >= 28:
                        frame_loop = [28, 31]
                
                if self.spell.name == "water_arrow" and self.moving:
                    frame_loop = [45, 54]
                
                img, frame = self.animation.animate("anim", True, True, loop_between= frame_loop)

                if self.spell.name == "attack":
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-2-scroll[0], self.colliders[0][0].y-2-scroll[1]))
                if self.spell.name == "fireball":
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-scroll[0], self.colliders[0][0].y-7-scroll[1]))
                if self.spell.name == "flame_slash":
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-2-scroll[0], self.colliders[0][0].y-scroll[1]))
                if self.spell.name == "splash":
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-2-scroll[0], self.colliders[0][0].y-scroll[1]))
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-2-scroll[0], self.colliders[0][0].y-scroll[1]))
                if self.spell.name == "drown":
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-2-scroll[0], self.colliders[0][0].y-scroll[1]))
                if self.spell.name == "ice_wall":
                    surf.blit(img, (self.colliders[0][0].x-3-scroll[0], self.colliders[0][0].y-scroll[1]))
                if self.spell.name == "water_arrow":
                    surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-6-scroll[0], self.colliders[0][0].y-scroll[1]))
                if self.spell.name == "flame_thrower":
                    if self.flip_x:
                        surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-8-scroll[0], self.colliders[0][0].y-scroll[1]))
                    else:
                        surf.blit(pygame.transform.flip(img, self.flip_x, self.flip_y), (self.colliders[0][0].x-scroll[0], self.colliders[0][0].y-scroll[1]))
                
            else:
                if self.spell.name == "fire rain":
                    for c, vel in self.colliders:
                        
                        pygame.draw.circle(self.gm.game.display, (160, 0, 0), [c.centerx-self.gm.camera.scroll[0], c.centery-self.gm.camera.scroll[1]], 4)
                        
                        for i in range(2):
                            if self.attack_time > 20:
                                v = [-vel[0]/2, -vel[1]/3]
                            else:
                                v = [0, -1]
                            p = Particle([c.centerx+random.randint(-2, 2), c.centery+random.randint(-2, 2)], v, 0, random.randint(4, 5), random.choice([(255, 0, 0), (255, 255, 0)]), 255)
                        
                            self.gm.particles.append(p)
                    
                if self.spell.name == "flame bombs" and not self.exploded:
                    for c, vel in self.colliders:
                        
                        pygame.draw.circle(self.gm.game.display, (160, 120, 80), [c.centerx-self.gm.camera.scroll[0], c.centery-self.gm.camera.scroll[1]], 3)
                        
                        if (self.attack_time % 10) == 0:
                            p = Particle([c.centerx+random.randint(-2, 2), c.centery+random.randint(-2, 2)], [-vel[0], vel[1]], 0, random.randint(4, 5), random.choice([(255, 0, 0), (255, 255, 0)]), 255)
                            
                            self.gm.particles.append(p)
                
            if self.gm.debug_render:
                for rect, _ in self.colliders:
                    pygame.draw.rect(surf, (120, 0,175), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
                    
                for rect in self.explosion_hitboxes:
                    pygame.draw.rect(surf, (120, 0,175), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
        
            

    def update(self):
        if self.active:
            if self.spell.duration.timed_out():
                self.spell.cast_cooldown.set()
            
            if self.spell.type in ["fire", "water", "lightning"] and self.spell.name ==  "attack":
                self.colliders[0][0].x += self.colliders[0][1][0]
                self.colliders[0][0].y += self.colliders[0][1][1]
                
                if self.spell.duration.timed_out():
                    self.active = False
                
            if self.spell.name in ["fireball", "flame_slash"]:
                self.colliders[0][0].x += self.colliders[0][1][0]
                self.colliders[0][0].y += self.colliders[0][1][1]
                
                if self.spell.duration.timed_out():
                    self.active = False
                
            if self.spell.name == "fire rain":
                for i, collider in sorted(enumerate(self.colliders), reverse=True):
                    c, vel = collider
                    if self.attack_time > 20:
                        c.x += vel[0]
                        c.y += vel[1]
                    
                    
                    for tile in self.gm.colliders["tiles"]:
                        if c.colliderect(tile):
                            try:
                                self.colliders.pop(i)
                            except:
                                pass
                    
                    if len(self.colliders) == 0:
                        self.active = False
                        self.spell.cast_cooldown.set()
            if self.spell.name == "flame bombs" and not self.exploded:
                for i, collider in sorted(enumerate(self.colliders), reverse=True):
                    c, vel = collider
                    c.x += vel[0]
                    c.y += vel[1]
                    
                    for tile in self.gm.colliders["tiles"]:
                        if c.colliderect(tile):
                            try:
                                self.colliders.pop(i)
                                self.exploded = True
                                self.attack_time = 0
                            except:
                                pass
                    
                    if self.spell.duration.timed_out():
                        self.exploded = True
                        self.attack_time = 0
                    
            if self.exploded:
                for collider in self.colliders:
                    c = collider[0]  
                    for i in range(60):
                        p = Particle(list(c.center), [random.uniform(-4, 4), random.uniform(-4, 4)], 5, random.randint(2, 7), random.choice([(255, 0, 0),(255, 255, 0)]), 255, deterioration=0.2)
                        self.gm.particles.append(p)
                    
                    r = pygame.FRect(0, 0, 80, 80)
                    r.center = c.center
                    self.explosion_hitboxes.append(r)
                
            if self.spell.name == "flame_thrower":
                self.flip_x = self.gm.player.flip
                
                self.colliders[0][0].topleft = [self.gm.player.rect.right+5, self.gm.player.rect.y]
                
                if self.flip_x:
                    self.colliders[0][0].topleft = [self.gm.player.rect.x-5-self.colliders[0][0].width, self.gm.player.rect.y]
                    
                                    
                if self.animation.frame_count+1 >= len(self.animation.frames["anim"]):
                    self.active = False
                    
            if self.spell.name == "splash":       
                if self.animation.frame_count+1 >= len(self.animation.frames["anim"]):
                    self.active = False
            
            if self.spell.name == "drown":                    
                if self.animation.frame_count+1 >= len(self.animation.frames["anim"]):
                    self.active = False
            
            if self.spell.name == "ice_wall":  
                if 28 <= self.animation.frame_count <= 31:
                    self.gm.colliders["tiles"].append(self.colliders[0][0])
                                  
                if self.animation.frame_count+1 >= len(self.animation.frames["anim"]):
                    self.active = False
            
            if self.spell.name == "water_arrow":
                if self.animation.frame_count+1 >= 40 and self.moving == False:
                    self.moving = True
                
                if self.moving:
                    self.colliders[0][0].x += self.colliders[0][1][0]
                    self.colliders[0][0].y += self.colliders[0][1][1]
                    
                    if self.spell.duration.timed_out():
                        self.active = False
        
        if self.spell.name in ["attack", "fireball", "flame_slash", "water_arrow"]:
            for rect, _ in self.colliders:
                for collider in self.gm.colliders["tiles"]:
                    if rect.colliderect(collider):
                        if self.spell.name == "water_arrow" and self.moving:
                            self.active = False
                            self.spell.cast_cooldown.set()
                        elif self.spell.name != "water_arrow":
                            self.active = False
                            self.spell.cast_cooldown.set()
        
        if self.exploded:
            if self.attack_time >= 2:
                self.active = False
        
        self.attack_time += 1
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
                    if spell.spell.name == "ice_wall":
                        pos = [self.gm.player.rect.left - 18, self.gm.player.rect.y-16]
                    if spell.spell.name == "water_arrow":
                        pos = [self.gm.player.rect.left - 41, self.gm.player.rect.y+9]
                        vel = [-1, 0]
                    if spell.spell.name == "flame_slash":
                        pos = [self.gm.player.rect.left - 7, self.gm.player.rect.y]
                        vel = [-8, 0]
                    if spell.spell.name == "flame bombs":
                        pos = [self.gm.player.rect.left - 5 -  random.randint(0, 3), self.gm.player.rect.centery-2]
                        vel = [-1, random.choice([-1, 1])]
                else:
                    if spell.spell.name == "fireball":
                        pos = [self.gm.player.rect.right + 5, self.gm.player.rect.y+9]
                        vel = [8, 0]
                    if spell.spell.name == "flame_slash":
                        pos = [self.gm.player.rect.right + 5, self.gm.player.rect.y]
                        vel = [8, 0]
                    if spell.spell.name == "water_arrow":
                        pos = [self.gm.player.rect.right + 5, self.gm.player.rect.y+9]
                        vel = [1, 0]
                    if spell.spell.name == "ice_wall":
                        pos = [self.gm.player.rect.right + 8, self.gm.player.rect.y-16]
                    if spell.spell.name == "flame bombs":
                        pos = [self.gm.player.rect.right + 5 + random.randint(0, 3), self.gm.player.rect.centery-2]
                        vel = [1, random.choice([-1, 1])]
                    
                if spell.spell.name == "fire rain":
                    pos = list(self.gm.player.rect.center)
                
                if spell.spell.name == "splash":
                    pos = list(self.gm.player.rect.topleft)
                if spell.spell.name == "drown":
                    pos = list(self.gm.player.rect.topleft)
                    pos[0] -= 16
                    pos[1] -= 32
                        
                spell.cast(pos, vel)
                self.spells.append(spell) 
    
    def draw(self):
        for i, spell in sorted(enumerate(self.spells), reverse=True):
            spell.draw(self.gm.game.display, self.gm.camera.scroll)
            
            if spell.active == False:
                self.spells.pop(i)
    
    def update(self):
        for mode in self.gm.player.spells:
            for sp in self.gm.player.spells[mode]:
                self.gm.player.spells[mode][sp].cast_cooldown.update()
        
        for i, spell in sorted(enumerate(self.spells), reverse=True):
            spell.update()
            
            if spell.active == False:
                self.spells.pop(i)



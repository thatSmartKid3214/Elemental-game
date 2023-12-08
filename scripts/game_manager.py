import pygame
import scripts.Engine as E
from scripts.player import Player
from scripts.world import World
import random
import json
from copy import deepcopy

class Game_Manager:
    def __init__(self, game):
        self.game = game
        self.assets = self.game.assets
        self.state = "Play"
        self.states = {"Play": self.play_game}
        self.player = Player(self, 704, 256, 16, 32, 4, 4.8, 0.2)
        self.camera = E.Camera()
        self.level = {"tiles":[],  "decor":[], "walls":[]}
        self.render_order = ["walls", "decor", "traps", "tiles"]
        self.TILESIZE = 16
        
        self.test_rects = []
        self.test_entries1 = []
        self.test_entries2 = []
        
        self.debug_render = False
        
        self.colliders = {"tiles":[], "l_ramps":[], "r_ramps":[], "platforms":[]}
        
        self.collidables = []
        for i in range(60):
            self.collidables.append(i+1)
        
        self.collidables = self.collidables + [90, 95, 96, 97]
        self.ramps = [91, 92]
        self.platforms = [87, 88, 89]
        self.spikes = []
        self.trapdoors = []
        self.animated_tiles = []
        self.doors = []
        
        self.world = World(self) 
        count = 15
        self.world.generate(count)    
        
        for i in range(self.world.max_retries):
            
            if self.world.retries >= self.world.max_retries:
                break
            
            if self.world.retry:
                print("retry")
                self.world.retry = False
                self.world.generate(count)
            elif self.world.retry == False:
                break  
        
        self.level = self.world.level
        
        pos = random.choice(self.world.spawn_points)
        
        self.player.set_pos(pos[0], pos[1])
        self.camera.update(self.player.rect, self.game.display, 1)
            
    def manage_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.close()
                
            if event.type == pygame.KEYDOWN: 
                
                if event.key == pygame.K_F1:
                    self.debug_render = not self.debug_render
                
                if event.key == pygame.K_1:
                    self.player.mode = "fire"
                    self.player.animation = self.player.animations[self.player.mode]
                if event.key == pygame.K_2:
                    self.player.mode = "water"
                    self.player.animation = self.player.animations[self.player.mode]
                if event.key == pygame.K_3:
                    self.player.mode = "lightning"
                    self.player.animation = self.player.animations[self.player.mode]
                
                if event.key == pygame.K_e:
                    if self.current_door != None:
                        if not self.current_door.locked:
                            self.current_door.closed = not self.current_door.closed
                            self.current_door.flip = self.player.flip
                                   
                if event.key == pygame.K_a:
                    self.player.left = True
                if event.key == pygame.K_d:
                    self.player.right = True
                if event.key == pygame.K_s:
                    if self.player.on_platform:
                        self.player.set_pos(self.player.rect.x, self.player.rect.y + 2)
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_LSHIFT:
                    self.player.animation.frame_count = 0
                    self.player.animation.set_loop(False)
                    self.player.dash()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player.left = False
                if event.key == pygame.K_d:
                    self.player.right = False
        
    def play_game(self):
        self.game.display.fill((127, 127, 127))
        self.game.clock.tick(self.game.fps)
        self.camera.update(self.player.rect, self.game.display, 5)
        scroll = self.camera.scroll
        
        render_range = [0, 0, 0, 0]
        
        c = 25
        render_range[0] = int((self.player.rect.left - self.TILESIZE*c)/self.TILESIZE)
        render_range[1] = int((self.player.rect.right + self.TILESIZE*c)/self.TILESIZE)
        render_range[2] = int((self.player.rect.top - self.TILESIZE*c)/self.TILESIZE) 
        render_range[3] = int((self.player.rect.bottom + self.TILESIZE*c)/self.TILESIZE)
        
        for layer in self.render_order:
            
            if layer == "decor":
                
                for animated_tile in self.animated_tiles:
                    if (render_range[0] < animated_tile[2][0] < render_range[1]) and (render_range[2] < animated_tile[2][1] < render_range[3]):
                        img = animated_tile[0].animate(animated_tile[1], True)
                        
                        self.game.display.blit(img, (animated_tile[2][0]*self.TILESIZE-scroll[0], animated_tile[2][1]*self.TILESIZE-scroll[1]))

                for d in self.doors:
                    if (render_range[0] < d.rect.x/self.TILESIZE < render_range[1]) and (render_range[2] < d.rect.y/self.TILESIZE < render_range[3]):
                        d.draw(self.game.display, scroll)
                        
                        if d.closed:
                            self.colliders["tiles"].append(d.rect)
                        
                        x = 0
                        if self.player.flip:
                            x = -16-(0.4*16)
                        else:
                            x = 16
                        
                        if pygame.Rect(self.player.rect.x+x, self.player.rect.y, self.player.rect.width*1.7, self.player.rect.height).colliderect(d.rect) and not self.player.rect.colliderect(d.rect):
                            self.current_door = d
                        
            if layer == "traps":
                for spike in self.spikes:
                    if (render_range[0] < spike.rect.x/self.TILESIZE < render_range[1]) and (render_range[2] < spike.rect.y/self.TILESIZE < render_range[3]):
                        spike.update()
                        
                        if self.player.rect.colliderect(spike.detection_rect) and spike.type == "hidden" and spike.active == False:
                            if spike.spike_id == 81 and (spike.rect.y == spike.pos[1]+16):
                                spike.active = True
                                spike.move_timer.set()
                            if spike.spike_id == 82 and (spike.rect.y == spike.pos[1]-8):
                                spike.active = True
                                spike.move_timer.set()
                            if spike.spike_id == 83 and (spike.rect.x == spike.pos[0]+16):
                                spike.active = True
                                spike.move_timer.set()
                            if spike.spike_id == 84 and (spike.rect.x == spike.pos[0]-8):
                                spike.active = True
                                spike.move_timer.set()
                        
                        if self.player.rect.colliderect(spike.rect):
                            pass
                        
                        spike.draw(self.game.display, scroll)
                
                for trapdoor in self.trapdoors:
                    trapdoor.update()
                    
                    if self.player.rect.bottom <= trapdoor.rect.y and not trapdoor.opened:
                        self.colliders["tiles"].append(trapdoor.rect)
                    
                        if pygame.Rect(self.player.rect.x, self.player.rect.y+2, self.player.rect.width, self.player.rect.height).colliderect(trapdoor.rect) \
                            and trapdoor.open_timer.timed_out() and self.player.collisions["bottom"]:
                                trapdoor.open_timer.set()
                    
                    trapdoor.draw(self.game.display, scroll)
                        
            if layer in self.level:
                for tile in self.level[layer]:    
                    if (render_range[0] < tile[1][0] < render_range[1]) and (render_range[2] < tile[1][1] < render_range[3]):
                        if tile[0] in self.assets.tileset:
                            self.game.display.blit(self.assets.tileset[tile[0]], (tile[1][0]*self.TILESIZE-scroll[0], tile[1][1]*self.TILESIZE-scroll[1]))

                            if tile[0] in self.collidables:
                                self.colliders["tiles"].append(pygame.Rect(tile[1][0]*self.TILESIZE, tile[1][1]*self.TILESIZE, self.TILESIZE, self.TILESIZE))

                            if tile[0] in self.platforms:
                                self.colliders["platforms"].append(pygame.Rect(tile[1][0]*self.TILESIZE, tile[1][1]*self.TILESIZE+2, self.TILESIZE, self.TILESIZE))
                            
                            if tile[0] == 92:
                                self.colliders["l_ramps"].append(pygame.Rect(tile[1][0]*self.TILESIZE, tile[1][1]*self.TILESIZE, self.TILESIZE, self.TILESIZE))
                            
                            if tile[0] == 91:
                                self.colliders["r_ramps"].append(pygame.Rect(tile[1][0]*self.TILESIZE, tile[1][1]*self.TILESIZE, self.TILESIZE, self.TILESIZE))
        
        
        for p in self.colliders["platforms"]:
            if self.player.rect.bottom <= p.y:        
                self.colliders["tiles"].append(p)
        
        self.player.move(self.colliders)
        self.player.update()
        
        if self.debug_render:
            for collision_layer in self.colliders:
                if collision_layer == "platforms":
                    continue
                for rect in self.colliders[collision_layer]:
                    pygame.draw.rect(self.game.display, (0, 255, 0), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
            for rect in self.test_rects:
                pygame.draw.rect(self.game.display, (255, 255, 255), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
            for rect in self.test_entries1:
                pygame.draw.rect(self.game.display, (255, 0, 0), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
            for rect in self.test_entries2:
                pygame.draw.rect(self.game.display, (255, 0, 255), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
        
        self.player.draw(self.game.display, scroll)
        self.manage_events()
        
        for c_id in self.colliders:
            self.colliders[c_id] = []
        self.current_door = None

        self.game.screen.blit( pygame.transform.scale(self.game.display, (self.game.screen.get_width() , self.game.screen.get_height())), (0, 0) )
        pygame.display.update()
     
    def run(self):
        self.states[self.state]()
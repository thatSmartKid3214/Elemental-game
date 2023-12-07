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
        self.render_order = ["walls", "decor", "tiles"]
        self.TILESIZE = 16
        self.count = 0
        
        self.test_rects = []
        self.test_entries1 = []
        self.test_entries2 = []
        
        self.debug_render = False
        
        self.colliders = {"tiles":[]}
        
        self.collidables = []
        for i in range(60):
            self.collidables.append(i+1)
        
        self.world = World(self) 
        count = 8
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
                
                if event.key == pygame.K_1:
                    self.player.mode = "fire"
                    self.player.animation = self.player.animations[self.player.mode]
                if event.key == pygame.K_2:
                    self.player.mode = "water"
                    self.player.animation = self.player.animations[self.player.mode]
                if event.key == pygame.K_3:
                    self.player.mode = "lightning"
                    self.player.animation = self.player.animations[self.player.mode]
                                   
                if event.key == pygame.K_a:
                    self.player.left = True
                if event.key == pygame.K_d:
                    self.player.right = True
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
                if event.key == pygame.K_w:
                    self.player.up = False
                if event.key == pygame.K_s:
                    self.player.down = False
        
    def play_game(self):
        self.game.display.fill((127, 127, 127))
        self.game.clock.tick(self.game.fps)
        self.camera.update(self.player.rect, self.game.display, 5)
        scroll = self.camera.scroll
        
        """
        if self.count%(self.game.fps) == 0:
            self.world.generate(30)
        """
        self.count += 1
        
        render_range = [0, 0, 0, 0]
        
        c = 25
        render_range[0] = int((self.player.rect.left - self.TILESIZE*c)/self.TILESIZE)
        render_range[1] = int((self.player.rect.right + self.TILESIZE*c)/self.TILESIZE)
        render_range[2] = int((self.player.rect.top - self.TILESIZE*c)/self.TILESIZE) 
        render_range[3] = int((self.player.rect.bottom + self.TILESIZE*c)/self.TILESIZE)
        
        for layer in self.render_order:
            for tile in self.level[layer]:    
                if (render_range[0] < tile[1][0] < render_range[1]) and (render_range[2] < tile[1][1] < render_range[3]):
                    if tile[0] in self.assets.tileset:
                        self.game.display.blit(self.assets.tileset[tile[0]], (tile[1][0]*self.TILESIZE-scroll[0], tile[1][1]*self.TILESIZE-scroll[1]))

                        if tile[0] in self.collidables:
                            self.colliders["tiles"].append(pygame.Rect(tile[1][0]*self.TILESIZE, tile[1][1]*self.TILESIZE, self.TILESIZE, self.TILESIZE))
        
        
        if self.debug_render:
            for rect in self.colliders["tiles"]:
                pygame.draw.rect(self.game.display, (0, 255, 0), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
            for rect in self.test_rects:
                pygame.draw.rect(self.game.display, (255, 255, 255), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
            for rect in self.test_entries1:
                pygame.draw.rect(self.game.display, (255, 0, 0), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
            for rect in self.test_entries2:
                pygame.draw.rect(self.game.display, (255, 0, 255), (rect.x-scroll[0], rect.y-scroll[1], rect.width, rect.height), 1)
        
        self.player.draw(self.game.display, scroll)
        self.manage_events()
        
        self.player.move(self.colliders["tiles"])
        self.player.update()
        
        self.colliders["tiles"] = []

        self.game.screen.blit( pygame.transform.scale(self.game.display, (self.game.screen.get_width() , self.game.screen.get_height())), (0, 0) )
        pygame.display.update()
     
    def run(self):
        self.states[self.state]()
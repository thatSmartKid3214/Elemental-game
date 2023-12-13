import pygame
import scripts.Engine as E
from scripts.spell import Spell, Spellcast
import math

class Player(E.Entity):
    def __init__(self, gm, x, y, width, height, vel, jump_height, gravity, anim_obj=None):
        super().__init__(x, y, width, height, vel, jump_height, gravity, anim_obj)
        self.gm = gm
        self.flip = False
        self.max_vel_y = 6
        self.jump_count = 0
        self.max_jumps = 1
        self.grounded = False
        
        self.on_wall = False
        self.wall_jumping = False
        self.jump_direction = 1
        
        self.can_dash = True
        self.dashing = False
        self.dash_speed = 10.6
        self.dash_direction = 1
        self.dash_timer = E.Timer(0.15, self.stop_dashing)
        self.dash_cooldown = E.Timer(0.4, self.refresh_dash)
        self.on_platform = False
        
        self.mode = "fire"
        
        idle_f_count = 24
        run_f_count = 4
        jump_f_count = [5, 3, 3, 3, 3, 5, 5, 5, 3, 3, 3]
        dash_f_count = 4
        attack_f_count = 11
        
        self.air_time = 0
        
        self.keys = 100
        
        self.on_l_ramp = False
        self.on_r_ramp = False
        
        f_anim = E.Animation()
        f_anim.load_anim(self.gm.assets.animations["fire"]["idle"], "idle", [idle_f_count] * 4)
        f_anim.load_anim(self.gm.assets.animations["fire"]["run"], "run",  [run_f_count]*12)
        f_anim.load_anim(self.gm.assets.animations["fire"]["jump"], "jump", jump_f_count)
        f_anim.load_anim(self.gm.assets.animations["fire"]["wall_slide"], "wall_slide", [1])
        f_anim.load_anim(self.gm.assets.animations["fire"]["dash"], "dash", [dash_f_count]*3)
        f_anim.load_anim(self.gm.assets.animations["fire"]["attack"], "attack", [attack_f_count]*4)
        w_anim = E.Animation()
        w_anim.load_anim(self.gm.assets.animations["water"]["idle"], "idle", [idle_f_count] * 4)
        w_anim.load_anim(self.gm.assets.animations["water"]["run"], "run",  [run_f_count]*12)
        w_anim.load_anim(self.gm.assets.animations["water"]["jump"], "jump", jump_f_count)
        w_anim.load_anim(self.gm.assets.animations["water"]["wall_slide"], "wall_slide", [1])
        w_anim.load_anim(self.gm.assets.animations["water"]["dash"], "dash", [dash_f_count]*3)
        w_anim.load_anim(self.gm.assets.animations["water"]["attack"], "attack", [attack_f_count]*4)
        l_anim = E.Animation()
        l_anim.load_anim(self.gm.assets.animations["lightning"]["idle"], "idle", [idle_f_count] * 4)
        l_anim.load_anim(self.gm.assets.animations["lightning"]["run"], "run",  [run_f_count]*12)
        l_anim.load_anim(self.gm.assets.animations["lightning"]["jump"], "jump", jump_f_count)
        l_anim.load_anim(self.gm.assets.animations["lightning"]["wall_slide"], "wall_slide", [1])
        l_anim.load_anim(self.gm.assets.animations["lightning"]["dash"], "dash", [dash_f_count]*3)
        l_anim.load_anim(self.gm.assets.animations["lightning"]["attack"], "attack", [attack_f_count]*4)
        
        self.animations = {"fire": f_anim, "water": w_anim, "lightning": l_anim}
        
        self.animation = self.animations[self.mode]
        self.state = "idle"
        self.flip = False
        self.jump_frame = "jump1"
        self.fall_anim = False
        
        s = Spell("fire", "attack", "Shoot a small fireball", 1, 10, 0.1, 5)
        s2 = Spell("water", "attack", "Shoot a small fireball", 1, 10, 0.1, 5)
        s3 = Spell("lightning", "attack", "Shoot a small fireball", 1, 10, 0.1, 5)
        
        self.test_spell = Spell("water", "ice_wall", "water, YAY!!!!", 1, 20, 4, 0, duration=3)
        test_spell2 = Spell("fire", "flame bombs", "explosive bombs", 1, 20, 0, count=10, duration=2)
        
        self.spells = {"fire":{"default": s, pygame.K_m: test_spell2}, "water":{"default":s2, pygame.K_n: self.test_spell}, "lightning":{"default":s3}}
        
        self.default_spell = self.spells[self.mode]["default"]
    
    def draw(self, surf, scroll=[0, 0]):
        
        mod_x = 24
        mod_y = 16
        
        if self.movement[0] == 0 and self.grounded and self.fall_anim == False:
            self.state = "idle"
        if self.dashing:
            self.state = "dash"
        elif self.dashing == False and self.grounded and self.fall_anim == False: 
            if self.movement[0] == 0:
                self.state = "idle"
            if self.movement[0] != 0:
                self.state = "run"
        
        if self.state == "wall_slide" and self.grounded:
            if self.movement[0] == 0:
                self.state = "idle"
            if self.movement[0] != 0:
                self.state = "run"
        
        if self.velocity[0] < -1:
            self.flip = True
        if self.velocity[0] > 1:
            self.flip = False
        
        self.jump_frame = ""
        if self.velocity[1] < 0 and self.on_wall == False:
            self.jump_frame = "jump1"
            self.state = "jump"
            self.animation.frame_count = 5
        
        if self.wall_jumping and self.on_wall == False:
            self.jump_frame = "jump1"
            self.state = "jump"
            self.animation.frame_count = 5
            
        if self.state in ["idle", "run", "wall_slide"] and self.grounded == False and self.on_wall == False:
            if self.air_time >= 30 and self.state == "run":
                self.animation.frame_count = 13
                self.state = "jump"
            if self.air_time >= 5 and self.state == "idle":
                self.animation.frame_count = 13
                self.state = "jump"
            if self.air_time >= 30 and self.state == "wall_slide":
                self.animation.frame_count = 13
                self.state = "jump"
        
        if self.state == "dash" and self.grounded == False and self.on_wall == False:
            if self.air_time >= 25 and self.dashing == False:
                self.animation.frame_count = 13
                self.state = "jump"
        
        if self.state == "dash" and self.grounded and self.on_r_ramp:
            if self.movement[0] == 0:
                self.state = "idle"
            if self.movement[0] != 0:
                self.state = "run"
        
        if self.state == "dash" and self.grounded and self.fall_anim:
            self.fall_anim = False
            if self.movement[0] == 0:
                self.state = "idle"
            if self.movement[0] != 0:
                self.state = "run"
        
        if self.wall_jumping and self.dashing:
            self.state = "dash"
            self.jump_frame = ""
            
        loop = None
        if self.fall_anim and not self.grounded:
            loop = [21, 31]
        
        if self.on_wall:
            self.state = "wall_slide"
            if self.flip:   
                mod_x = 21
            if self.flip == False:
                mod_x = 27
        
        self.image, f = self.animation.animate(self.state, True, True, set_frame=self.jump_frame, loop_between=loop)
        
        if self.state == "jump" and self.animation.frame_count >= len(self.animation.frames["jump"])-1:
            #print("Yolo")
            self.fall_anim = False
            self.state = "idle"
        
        if self.state == "jump" and f == "jump6":
            self.fall_anim = True
        
        surf.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x-mod_x-scroll[0],self.rect.y-mod_y-scroll[1]))
        
        if self.gm.debug_render:
            pygame.draw.rect(surf, (255, 255, 255), (self.rect.x-scroll[0],self.rect.y-scroll[1], self.rect.width, self.rect.height), 1)
    
    
    def stop_dashing(self):
        self.animation.set_loop(True)
        self.dashing = False
    
    def refresh_dash(self):
        self.can_dash = True
    
    def dash(self):
        if self.can_dash:
            self.dashing = True
            self.can_dash = False
            self.dash_timer.set()
            self.dash_cooldown.set()
    
    def jump(self):
        if self.on_wall:
            self.velocity[0] = 4.8 * self.jump_direction
            self.velocity[1] = -3.2
            self.wall_jumping = True
        elif self.jump_count < self.max_jumps and self.on_wall == False:
            self.jump_count += 1
            self.velocity[1] = -self.jump_height
            self.grounded = False
        
    def move(self, colliders):
        self.movement = [0, 0]
        grav_modifier = 1
        if self.left:
            self.movement[0] = -self.vel
            self.flip = True
            self.dash_direction = -1
            if self.grounded and self.fall_anim == False:
                self.state = "run"
        if self.right:
            self.movement[0] = self.vel
            self.flip = False
            self.dash_direction = 1
            if self.grounded and self.fall_anim == False:
                self.state = "run"
        self.velocity[1] += self.gravity
        if self.up:
            self.movement[1] = -self.vel
        if self.down:
            self.movement[1] = self.vel
        
        if self.velocity[1] >= 0:
            grav_modifier = 1.1
        elif self.velocity[1] < 0:
            grav_modifier = 1
            
        self.velocity[1] = min(self.velocity[1] * grav_modifier, self.max_vel_y)
        
        if (self.velocity[0] > 2.2) or (self.velocity[0] < -2.2):
            self.movement[0] = 0
            
        movement = [self.movement[0] + self.velocity[0], self.movement[1] + self.velocity[1]]
        
        if self.velocity[0] > self.vel:
            self.movement[0] = min(self.vel, self.movement[0])
        if self.velocity[0] < -self.vel:
            self.movement[0] = max(-self.vel, self.movement[0])
        
        #print(movement)
        
        # Wall sliding
        if self.on_wall == True:
            if self.velocity[1] > 0.3:
                self.velocity[1] = 0.3
        
        #Dashing
        if self.grounded or self.velocity[0] < -1 or self.velocity[0] > 1:
            if self.flip:
                self.dash_direction = -1
            if not self.flip:
                self.dash_direction = 1
        
        if self.dashing:
            movement[0] = self.dash_speed * self.dash_direction
            self.velocity[1] = 0
        
        platform_list = E.collision_test(pygame.Rect(self.rect.x, self.rect.y+1, self.rect.width, self.rect.height), colliders["platforms"])
        if len(platform_list) > 0:
            self.on_platform = True
        else:
            self.on_platform = False
        
        if not self.grounded:
            self.air_time += 1
        
        self.collisions = self.physics_obj.movement(movement, colliders["tiles"], colliders["l_ramps"], colliders["r_ramps"])
        self.rect.center = self.physics_obj.rect.center
        
        self.on_l_ramp = len(E.collision_test(self.rect, colliders["l_ramps"])) > 0
        self.on_r_ramp = len(E.collision_test(self.rect, colliders["r_ramps"])) > 0

        self.on_wall = False
        
        if self.collisions["bottom"]:
            self.velocity[1] = 0.8
            self.jump_count = 0
            if self.fall_anim and self.state == "jump":
                if self.animation.frame_count < 32:
                    self.animation.frame_count = 32
                    #self.fall_anim = False
            self.grounded = True
            self.air_time = 0
        else:
            self.grounded = False
        
        if self.collisions["top"]:
            self.velocity[1] = 1
        
        if self.collisions["right"] and self.grounded == False and self.dashing == False:
            self.on_wall = True
            self.jump_direction = -1
            self.flip = True
        
        if self.collisions["left"] and self.grounded == False and self.dashing == False:
            self.on_wall = True
            self.jump_direction = 1
            self.flip = False
        
        # Cap the velocity in the x direction
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.2, 0)
        if self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.2, 0)
        
        if self.velocity[0] == 0:
            self.wall_jumping = False
    
    def update(self):
        self.test_spell.cast_cooldown.update()
        self.dash_timer.update()
        self.dash_cooldown.update()




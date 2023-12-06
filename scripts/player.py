import pygame
import scripts.Engine as E

class Player(E.Entity):
    def __init__(self, x, y, width, height, vel, jump_height, gravity, anim_obj=None):
        super().__init__(x, y, width, height, vel, jump_height, gravity, anim_obj)
        self.flip = False
        self.max_vel_y = 6
        self.jump_count = 0
        self.max_jumps = 1
        self.grounded = False
        
        self.on_wall = False
        self.jump_direction = 1
        
        self.can_dash = True
        self.dashing = False
        self.dash_speed = 12
        self.dash_direction = 1
        self.dash_timer = E.Timer(0.1, self.stop_dashing)
        self.dash_cooldown = E.Timer(1, self.refresh_dash)
        
    
    def stop_dashing(self):
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
            self.velocity[0] = 5.8 * self.jump_direction
            self.velocity[1] = -3.2
        elif self.jump_count < self.max_jumps and self.on_wall == False:
            self.jump_count += 1
            self.velocity[1] = -self.jump_height
            self.grounded = False
        
    def move(self, tiles):
        self.movement = [0, 0]
        grav_modifier = 1
        if self.left:
            self.movement[0] = -self.vel
            self.flip = True
            self.dash_direction = -1
        if self.right:
            self.movement[0] = self.vel
            self.flip = False
            self.dash_direction = 1
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
            if self.velocity[1] > 0.6:
                self.velocity[1] = 0.6
        
        #Dashing
        if self.dashing:
            movement[0] = self.dash_speed * self.dash_direction
            self.velocity[1] = 0
        
        self.collisions = self.physics_obj.movement(movement, tiles)
        self.rect.center = self.physics_obj.rect.center

        self.on_wall = False
        
        if self.collisions["bottom"]:
            self.velocity[1] = 1
            self.jump_count = 0
            self.grounded = True
        
        if self.collisions["top"]:
            self.velocity[1] = 1
        
        if self.collisions["right"] and self.grounded == False:
            self.on_wall = True
            self.jump_direction = -1
        
        if self.collisions["left"] and self.grounded == False:
            self.on_wall = True
            self.jump_direction = 1
        
        # Cap the velocity in the x direction
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.2, 0)
        if self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.2, 0)
    
    def update(self):
        self.dash_timer.update()
        self.dash_cooldown.update()




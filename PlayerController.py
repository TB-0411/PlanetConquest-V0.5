import math
import random
import time

import Settings
import Main
import Util

class Player():
    def __init__(self, game):
        self.game = game
        self.sprite = None
        
        self.current_planet = None
        self.clockwise = False
        
        self.life = 100
        self.immune = 0
        
        self.distance = 0
        self.orbit_angle = 0
        self.velocity = 0.7
        self.celerity = 0.7
        self.trajectory = (0,0,0)
        
        self.player_stats = {}
        self.player_stats['score'] = 0   
        
    def explode(self):
        self.game.explosion_sprite.position = self.sprite.position
        self.game.explosion_sprite.visible = True
        self.die()
        
    def die(self):
        self.sprite.visible = False
        self.sprite.stop()
        self.life = 0
        
    def life_check(self):
        if self.life > 0 and not self.sprite.visible: 
            self.sprite.visible = True
            self.velocity = 0.3
            self.celerity = 0.7
        if self.velocity > 100 or self.velocity < -10: self.explode()
        
    def collision_check(self) -> bool:
        if self.immune > 0: self.immune -= 1; return False
        collision = self.sprite.collides_with_list(self.game.scene.get_sprite_list("Planets"))
        border = self.sprite.collides_with_list(self.game.scene.get_sprite_list("Borders"))
        
        if collision: 
            if collision[0] == self.current_planet: return False
            print("Collide at : ",self.sprite.position)
            self.change_orbit(collision[0])
            self.immune = 100
            return True
        
        elif border:
            if (self.trajectory[2] % 90 == 0): self.trajectory = (-self.trajectory[0], -self.trajectory[1], Util.get_trajectory_angle(-self.trajectory[0],-self.trajectory[1]))
            elif (self.trajectory[2] % 90 != 0):
                if border[0].center_y == Settings.SCREEN_HEIGHT//2: self.trajectory = (-self.trajectory[0], self.trajectory[1], Util.get_trajectory_angle(-self.trajectory[0],self.trajectory[1]))
                elif border[0].center_x == Settings.SCREEN_WIDTH//2: self.trajectory = (self.trajectory[0], -self.trajectory[1], Util.get_trajectory_angle(self.trajectory[0],-self.trajectory[1]))
                    
            self.sprite.face_point((self.sprite.center_x + self.trajectory[0], self.sprite.center_y + self.trajectory[1])) 
            self.sprite.angle = Util.convert_to_sprite_angle( Util.get_facing_angle(self.sprite.angle, self.clockwise) )
            self.immune = 3
            return True
            
    def change_orbit(self,new_orbit):
        self.game.space.checkBoundaries()
        self.game.space._populate_secret()
        
        self.sprite.stop()
        self.velocity -= 0.1
        self.celerity = 0.7
        self.distance = 0
                
        if self.current_planet != None: self.current_planet.return_trajectory = None
        self.current_planet = new_orbit
        self.orbit_angle = Util.get_angle_from_points(self.current_planet.center_x, self.current_planet.center_y, self.sprite.center_x, self.sprite.center_y)
        angle = Util.contain_angle(self.sprite.angle - 270)
        
        print('Orbit :', self.orbit_angle, angle)

        ''' Def if clockwise '''
        angle_between = (max(self.orbit_angle, angle) - min(self.orbit_angle, angle)) #Get the angle between the Planet/Rocket vector and the LastPlanet/Rocket vector
        #print(self.orbit_angle,(self.sprite.angle - 270),angle_between)
        if angle_between <= 90 : self.clockwise = not self.clockwise
        #print(self.clockwise, angle_between)

        if self.clockwise: index = 1
        else: index = 0
                
        self.sprite.texture = self.sprite.textures[index] #Flip texture when needed
        
    def move(self):
        if self.current_planet != None: 
            if self.velocity > 0.7: self.velocity -= 0.0001*random.randint(1,6)
            if self.celerity < 1.3: self.celerity += 0.001*self.velocity
            
            self.sprite.position = (round(self.current_planet.center_x + (self.current_planet.collision_radius * self.celerity) * math.cos(math.radians(self.orbit_angle)), 0),
                                    round(self.current_planet.center_y + (self.current_planet.collision_radius * self.celerity) * math.sin(math.radians(self.orbit_angle))), 0)
            self.sprite.face_point(self.current_planet.position)
            
            if math.dist((self.current_planet.position[0],self.current_planet.position[1]), Settings.SCREEN_CENTER) > 1:
                self.immune = 100
                if self.current_planet.return_trajectory == None:
                    angle = Util.get_angle_from_points(self.current_planet.center_x,self.current_planet.center_y,Settings.SCREEN_CENTER[0],Settings.SCREEN_CENTER[1])
                    print(angle)
                    self.current_planet.return_trajectory = Util.get_trajectory(angle)
                    
                self.game.space.move(self.current_planet.return_trajectory, self.velocity)
                
            if not self.clockwise : self.orbit_angle += 1 * self.velocity
            else: self.orbit_angle -= 1 * self.velocity
        else: 
            if self.velocity < 1.3: self.velocity += 0.001*random.randint(1,6)
            
            self.distance += (abs(self.trajectory[0])+abs(self.trajectory[1]))/2
            if self.distance > Settings.UNLOAD_RADIUS//10: 
                self.game.space.checkBoundaries()
                self.game.space._populate_secret()
                self.distance = 0
                
            #self.sprite.position = (self.sprite.position[0]+(self.trajectory[0] * self.velocity), self.sprite.position[1]+(self.trajectory[1] * self.velocity))
            self.game.space.move((-self.trajectory[0],-self.trajectory[1]),self.velocity)
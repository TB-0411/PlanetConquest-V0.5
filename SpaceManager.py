import math
import random
import arcade
import os

import Settings
import Util
import Main 

class Space():
    def __init__(self, game):
        self.game = game
        self.planets = self.game.scene.get_sprite_list('Planets')
        self.unloaded_planets = []
        self.planets_with_moons = []
        
    def move(self,trajectory,velocity):
        for p in self.game.scene.get_sprite_list('Planets'):
            p.position = (p.position[0]+(trajectory[0] * velocity), p.position[1]+(trajectory[1] * velocity))
        
    def checkBoundaries(self):
        for p in self.planets:
            dist = math.dist(Settings.SCREEN_CENTER, p.position)
            if dist > Settings.KILL_RADIUS: p.kill()
            elif dist > Settings.UNLOAD_RADIUS: 
                p.visible = False
                self.unloaded_planets.append(p)
                self.planets.remove(p)
            elif not p.visible and dist < Settings.UNLOAD_RADIUS - Settings.MIN_PLANET_DIST: 
                p.visible = True
                self.unloaded_planets.remove(p)
                self.planets.append(p)
            
    def generate_planet(self, p):
        scale_factor = random.randint(3,6)/10
        planet = arcade.Sprite(os.path.join(os.path.dirname(__file__),"assets\EmptyPlanet2.png"), scale_factor)
        planet.color = (random.randint(25,230),random.randint(25,230),random.randint(25,230))
        planet.center_x = p[0]
        planet.center_y = p[1]
        
        planet.return_trajectory = None
            
        planet.angle = Util.convert_to_sprite_angle(random.randint(0,360))
        planet.collision_radius = scale_factor * Settings.PLANET_SIZE

        self.unloaded_planets.append(planet)
        self.game.scene.add_sprite("Planets", planet)
        return planet
    
    def populate(self,x_area,y_area):
        points = []  
        tries = 0
        while tries < 100:
            tries += 1
            
            x = random.randint(x_area[0], x_area[1])
            y = random.randint(y_area[0], y_area[1])
            
            new_point = (x,y)
            too_close = False

            for p in points:
                if (math.dist(p, new_point) < Settings.MIN_PLANET_DIST):
                    too_close = True
                    break
                
            for up in self.unloaded_planets:
                if (math.dist(up.position, new_point) < Settings.MIN_PLANET_DIST):
                    too_close = True
                    break

            if (too_close): continue
            points.append(new_point)
            
        for p in points:
            self.generate_planet(p)
            
        self.checkBoundaries()
        
    def _populate(self):
        x_area = (-Settings.UNLOAD_RADIUS + Settings.SCREEN_WIDTH//2, Settings.UNLOAD_RADIUS + Settings.SCREEN_WIDTH//2)
        y_area = (-Settings.UNLOAD_RADIUS + Settings.SCREEN_HEIGHT//2, Settings.UNLOAD_RADIUS + Settings.SCREEN_HEIGHT//2)
        self.populate(x_area,y_area)
        
            
    def _populate_secret(self):
        x_area = (-Settings.UNLOAD_RADIUS + Settings.SCREEN_WIDTH//2, -Settings.MIN_PLANET_DIST)
        y_area = (-Settings.UNLOAD_RADIUS + Settings.SCREEN_HEIGHT//2, Settings.UNLOAD_RADIUS + Settings.SCREEN_HEIGHT//2)
        self.populate(x_area,y_area)
        
        x_area = (-Settings.UNLOAD_RADIUS + Settings.SCREEN_WIDTH//2, Settings.UNLOAD_RADIUS + Settings.SCREEN_WIDTH//2)
        y_area = (-Settings.UNLOAD_RADIUS + Settings.SCREEN_HEIGHT//2, -Settings.MIN_PLANET_DIST)
        self.populate(x_area,y_area)
        
        x_area = (Settings.MIN_PLANET_DIST + Settings.SCREEN_WIDTH, Settings.UNLOAD_RADIUS + Settings.SCREEN_WIDTH//2)
        y_area = (-Settings.UNLOAD_RADIUS + Settings.SCREEN_HEIGHT//2, Settings.UNLOAD_RADIUS + Settings.SCREEN_HEIGHT//2)
        self.populate(x_area,y_area)
        
        x_area = (-Settings.UNLOAD_RADIUS + Settings.SCREEN_WIDTH//2, Settings.UNLOAD_RADIUS + Settings.SCREEN_WIDTH//2)
        y_area = (Settings.MIN_PLANET_DIST + Settings.SCREEN_HEIGHT, Settings.UNLOAD_RADIUS + Settings.SCREEN_HEIGHT//2)
        self.populate(x_area,y_area)
import arcade
import time
import os

import Util
import PlayerController
import SpaceManager
import Settings

class PlanetConquestGame(arcade.Window):
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT, Settings.SCREEN_TITLE, False, False, (1/Settings.MAX_FPS))
        self.scene = None
        self.explosion_sprite = None
        
        self.keys_holded = {}
        
        self.space = None
        self.player = PlayerController.Player(self)
        
        arcade.set_background_color(arcade.csscolor.BLACK)

    # Called when restarted the game
    def setup(self):
        # Setup Scene
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Planets", use_spatial_hash=True)
        self.scene.add_sprite_list("Players")
        self.scene.add_sprite_list("Explosions")
        self.scene.add_sprite_list("Borders", use_spatial_hash=True)
        
        # Setup Player Sprite
        self.player.sprite = arcade.Sprite()
        self.player.sprite.scale = Settings.CHARACTER_SCALING
        self.player.sprite.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture(os.path.join(os.path.dirname(__file__),"assets\SpaceRocket.png"))
        self.player.sprite.textures.append(texture)
        texture = arcade.load_texture(os.path.join(os.path.dirname(__file__),"assets\SpaceRocket.png"),flipped_horizontally=True)
        self.player.sprite.textures.append(texture)
        # By default, face right.
        self.player.sprite.texture = texture
        
        self.player.sprite.center_x = Settings.SCREEN_WIDTH // 2
        self.player.sprite.center_y = Settings.SCREEN_HEIGHT // 2
        self.player.sprite.collision_radius = Settings.CHARACTER_SCALING * 110
        self.scene.add_sprite("Players", self.player.sprite)
        
        #Initialise Explosion Sprite
        self.explosion_sprite = arcade.Sprite()
        self.explosion_sprite.scale = 0.3
        self.explosion_sprite.textures = []
        self.explosion_sprite.animation_key = 0
        for i in range(1,6):
            texture = arcade.load_texture(os.path.join(os.path.dirname(__file__),"assets\Explosion"+str(i)+".png"))
            self.explosion_sprite.textures.append(texture)
        self.explosion_sprite.texture = self.explosion_sprite.textures[0]
        self.explosion_sprite.visible = False
        self.scene.add_sprite("Explosions", self.explosion_sprite)
        
        # Generate Planets
        self.space = SpaceManager.Space(self)
        
        planet = self.space.generate_planet(Settings.SCREEN_CENTER)
        self.player.current_planet = planet
        self.player.change_orbit(planet)
        
        self.space._populate()
        self.space.checkBoundaries()
            
        # Place Borders
        for x in range(4):
            wall = arcade.Sprite(os.path.join(os.path.dirname(__file__),"assets\Border.png"), 1)
            wall.center_x = (Settings.SCREEN_WIDTH // 2) * abs(x-1) #Mid 0 Mid 1
            wall.center_y = (Settings.SCREEN_WIDTH//2) * abs(x-1)   #0 Mid 1 Mid
            if x < 2: wall.center_y += (Settings.SCREEN_WIDTH//2)
            else: wall.center_y -= (Settings.SCREEN_WIDTH//2)
            wall.angle = 90 * abs(x%2)
            self.scene.add_sprite("Borders", wall)
            
        # END
    
    def on_key_hold(self):
        if self.keys_holded.get(arcade.key.DOWN): self.player.velocity -= 0.1 
        if self.keys_holded.get(arcade.key.UP): self.player.velocity += 0.1   
        if self.keys_holded.get(arcade.key.RIGHT): Settings.TIME_FACTOR += 0.01
        if self.keys_holded.get(arcade.key.LEFT): 
            if Settings.TIME_FACTOR > 0.01: Settings.TIME_FACTOR -= 0.01
        
    def on_key_press(self, symbol, modifier): 
        # Leave current orbit
        if symbol == arcade.key.SPACE: 
            print("Here we go : ",end='')
            
            angle = Util.get_facing_angle(self.player.sprite.angle, self.player.clockwise)
            self.player.trajectory = Util.get_trajectory(angle)
            print(self.player.trajectory)
            
            self.player.current_planet.return_trajectory = None
            self.player.current_planet = None
            
        if symbol == arcade.key.UP: self.keys_holded[arcade.key.UP] = True
        if symbol == arcade.key.DOWN: self.keys_holded[arcade.key.DOWN] = True
        if symbol == arcade.key.RIGHT: self.keys_holded[arcade.key.RIGHT] = True
        if symbol == arcade.key.LEFT: self.keys_holded[arcade.key.LEFT] = True
        
        # Fuck Go BAck
        if symbol == arcade.key.ENTER: 
            self.player.life = 100
            self.player.sprite.position = Settings.SCREEN_CENTER
            self.player.sprite.texture = self.player.sprite.textures[self.player.sprite.textures.index(self.player.sprite.texture)-1]
            self.player.trajectory = (-self.player.trajectory[0],-self.player.trajectory[1],self.player.trajectory[2])
  
    def on_key_release(self, symbol, modifier): 
        if symbol == arcade.key.UP: self.keys_holded[arcade.key.UP] = False
        if symbol == arcade.key.DOWN: self.keys_holded[arcade.key.DOWN] = False
        if symbol == arcade.key.RIGHT: self.keys_holded[arcade.key.RIGHT] = False
        if symbol == arcade.key.LEFT: self.keys_holded[arcade.key.LEFT] = False
        
    def on_update(self, delta_time):     
        time.sleep((1/(Settings.FPS*Settings.TIME_FACTOR)))
         
        if self.player.life <= 0: return
        self.on_key_hold()
        
        self.player.collision_check()
        self.player.move()
        self.player.life_check()
        
    def explosions_animation(self):
        if self.explosion_sprite.animation_key > 4: 
            self.explosion_sprite.animation_key = 0
            self.explosion_sprite.visible = False
            self.explosion_sprite.scale = 0.3
        if self.explosion_sprite.visible: 
            self.explosion_sprite.angle = self.player.sprite.angle
            self.explosion_sprite.texture = self.explosion_sprite.textures[self.explosion_sprite.animation_key]
            self.explosion_sprite.animation_key += 1
            factor = (0.03*self.explosion_sprite.animation_key)
            self.explosion_sprite.scale += factor/3
            time.sleep(0.1+factor)

    def print_stats(self):
        arcade.enable_timings = True
        arcade.draw_text('P:'+str( len( self.scene.get_sprite_list('Planets') ) ) 
                        +' '+ 'A:'+str( round( Util.get_facing_angle(self.player.sprite.angle, self.player.clockwise),0 ) ) 
                        +' '+ 'V:'+str( round( self.player.velocity,1 ) )
                        +'   '+ 'T:'+str( round( Settings.TIME_FACTOR,2 ) ),
                        5, 5, arcade.color.YELLOW, 12)
        arcade.enable_timings = False

    def on_draw(self):
        """Render the screen."""
        # Clear the screen to the background color
        self.clear()
        # Draw our sprites
        self.explosions_animation()
        self.scene.draw()
        # Print stats
        self.print_stats()
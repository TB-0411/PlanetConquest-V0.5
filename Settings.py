import arcade

import Main

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_CENTER = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
SCREEN_TITLE = "Space Pioneers"

CHARACTER_SCALING = 0.1
PLANET_SIZE = 145
ATMOSPHERE_SIZE = 40

GRAVITY = 0
ORBIT_DIST = 1.2
MIN_PLANET_DIST = 100 + ATMOSPHERE_SIZE

UNLOAD_RADIUS = (SCREEN_WIDTH + SCREEN_HEIGHT)//2 + MIN_PLANET_DIST
KILL_RADIUS = UNLOAD_RADIUS * 1.2

FPS = 120
MAX_FPS = 1024
TIME_FACTOR = 1.0

""" Launcher """

game = None

def main():
    game = Main.PlanetConquestGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
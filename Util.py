import math
'''Util functions'''
def contain_angle(angle): # Keeps angles right in between 0 and 360
    while angle < 0: angle += 360
    while angle > 360: angle -= 360
    return angle

def convert_to_sprite_angle(angle):
    sprite_angle = angle + 90
    return contain_angle(sprite_angle)
            
def convert_from_sprite_angle(sprite_angle):
    angle = sprite_angle - 90
    return contain_angle(angle)
    
def get_facing_angle(sprite_angle,is_clockwise):
    angle = convert_from_sprite_angle(sprite_angle)
    if is_clockwise: angle -= 90
    else: angle += 90
    return contain_angle(angle)

def get_trajectory_angle(x,y): # Get the angle of a point from the center
    angle = math.degrees(math.atan2(x,y))
    return contain_angle(angle)
    
def get_trajectory(angle):
    return (math.cos( math.radians(angle) ),math.sin( math.radians(angle) ), angle)
    
def get_angle_from_points(x1,y1,x2,y2):
    angle = math.atan2( y2 - y1, x2 - x1 ) * ( 180 / math.pi ) 
    return contain_angle(angle)
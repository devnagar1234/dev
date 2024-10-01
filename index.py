from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Configuration
jump_height = 2.5  # Maximum height of the jump
jump_duration = 0.8  # Duration of the jump
gravity_scale = 1  # Gravity affecting the player
mouse_sensitivity = Vec2(40, 40)
run_speed = 5

window.fps_counter.enabled = False
window.exit_button._visible = True 

# Audio
punch = Audio('assets/punch.wav', autoplay=False)

# Textures
blocks = [
    load_texture('grass.png'),  # 0
    load_texture('stone.png'),  # 1
    load_texture('gold.png'),   # 2
    load_texture('lava.png'),   # 3
]

block_id = 1  # Default block

# Hand entity
hand = Entity(
    parent=camera.ui,
    model='block_texture.psd',
    texture=blocks[block_id],
    scale=0.2,
    rotation=Vec3(-10, -10, 10),
    position=Vec2(0.6, -0.6)
)

# Sky entity
sky = Entity(
    parent=scene,
    model='sphere',
    texture=load_texture('sky.jpg'),
    scale=500,
    double_sided=True
)

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture='grass.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='block.obj',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])
            elif key == 'right mouse down':
                destroy(self)

def create_parcour():
    """ Create a parcour with obstacles and checkpoints. """
    # Create a long platform
    for z in range(10):
        for x in range(50):
            Voxel(position=(x, 0, z), texture='grass.png')
    
    # Add obstacles and checkpoints
    for x in range(2, 50, 3):  # Adding obstacles every 10 blocks
        Voxel(position=(x, 1, 1), texture='stone.png')  # Obstacles
     
    # Place a starting point
    Voxel(position=(0, 1, 0), texture='grass.png')


        # Add obstacles and checkpoints
    for x in range(2, 50, 4):  # Adding obstacles every 10 blocks
        Voxel(position=(x, 1, 1), texture='gold.png')
        # Checkpoints

    # Place a starting point

    Voxel(position=(0, 1, 0), texture='gold.png')


    for x in range(2, 50, 4):  # Adding obstacles every 10 blocks
        Voxel(position=(x, 1, 3), texture='.png')
        # Checkpoints

    # Place a starting point

    Voxel(position=(0, 1, 0), texture='gold.png')

def reset_game():
    """ Teleport the player back to the start position. """
    player.position = (0, 1, 0)
    player.rotation = (0, 0, 0)  # Optional: Reset player rotation if needed

# Initialize game
create_parcour()

player = FirstPersonController()
player.jump_height = jump_height
player.jump_up_duration = jump_duration
player.gravity = gravity_scale
player.mouse_sensitivity = mouse_sensitivity
player.speed = run_speed

def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)

    if player.y < -10:  # Check if the player falls below a certain height
        print("Press 'R' to retry")  # Notify player to press 'R' to retry

def input(key):
    global block_id
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id]
    elif key == 'r':  # Check if 'R' key is pressed
        reset_game()  # Call the reset game function

app.run()

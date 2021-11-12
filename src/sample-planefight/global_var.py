from pygamescratch import *


CALL_FRIEND_KEY = K_l
PAUSE_KEY = K_SPACE
FIRE_TRIPLE_KEY = K_k
FIRE_SINGLE_KEY = K_j
DIRECTION_UP_KEY = K_w
DIRECTION_DOWN_KEY = K_s
DIRECTION_LEFT_KEY = K_a
DIRECTION_RIGHT_KEY = K_d

enemy0_down_count = 1
pending_enemy_types = []
EVENT_ENEMY_DOWN = "_EVENT_ENEMY_DOWN"
enemy_hp_rate = 3
max_hp = 10
max_bullets = 25

max_enemies = 15

score = 0
font_name = "./font/hkwawa.ttc"

friend_fire_wait = 0.5
friend_change_direction_wait = 0.1
enemy_initial_fire_wait = 5
enemy_initial_new_wait = 2
enemy_fire_wait = 5
enemy_new_wait = 2

hero = None

def get_enemies():
    sprites = get_sprites_by_name("enemy0")
    sprites.extend(get_sprites_by_name("enemy1"))
    sprites.extend(get_sprites_by_name("enemy2"))
    return sprites
from pygamescratch import *

CALL_FRIEND_KEY = K_l
PAUSE_KEY = K_SPACE
RESTART_KEY = K_RETURN
FIRE_TRIPLE_KEY = K_k
FIRE_SINGLE_KEY = K_j
DIRECTION_UP_KEY = K_w
DIRECTION_DOWN_KEY = K_s
DIRECTION_LEFT_KEY = K_a
DIRECTION_RIGHT_KEY = K_d
BULLET_TYPE_HERO = 1
BULLET_TYPE_FRIEND = 2


class GlobalV:

    def __init__(self):
        self.enemy0_down_count = 1
        self.pending_enemy_types = []
        self.enemy_hp_rate = 4
        self.max_hp = 10
        self.max_bullets = 25

        self.max_enemies = 15

        self.score = 0
        self.font_name = "./font/hkwawa.ttc"

        self.friend_fire_wait = 0.25
        self.friend_change_direction_wait = 0.1
        self.enemy_initial_fire_wait = 3
        self.enemy_initial_new_wait = 2
        self.enemy_fire_wait = 5
        self.enemy_new_wait = 2

        self.hero = None
        self.obstacle = None
        self.pause_icon = None

    def display_hero_hp(self):
        if self.hero is None:
            return
        # 显示血条
        hero_hp = self.hero.hp
        hp_sprites = pygs.get_sprites_by_name("hp")
        if len(hp_sprites) <= 0:
            x = 10
            for index in range(0, self.max_hp + 1):
                Sprite("hp", x + index * 25, pygs.max_y - 50)
            hp_sprites = pygs.get_sprites_by_name("hp")
        for index in range(1, len(hp_sprites) + 1):
            hp_sprites[index - 1].showing = (index <= hero_hp)

    def display_hero_bullet_score(self):
        if self.hero is None:
            return
        max_hero_bullets = self.hero.max_hero_bullets
        display_text = "分数：{0}".format(self.score)
        pygs.text("score_text", display_text, x=pygs.max_x - 110, y=pygs.max_y - 30, size=22, color=(128, 128, 128))
        remaining_bullets = max_hero_bullets - len(self.get_hero_bullets())
        pygs.text("bullet_text", "弹药：{0}".format(remaining_bullets), x=5, y=pygs.max_y - 30, size=18, color=(0, 0, 0))

    def get_enemies(self):
        sprites = pygs.get_sprites_by_name("enemy0")
        sprites.extend(pygs.get_sprites_by_name("enemy1"))
        sprites.extend(pygs.get_sprites_by_name("enemy2"))
        return sprites

    def get_hero_bullets(self):
        bullets = pygs.get_sprites_by_name("herobullet")
        hero_bullets = list(filter(lambda b: b.bullet_type == BULLET_TYPE_HERO, bullets))
        return hero_bullets


g = GlobalV()

from friend_plane import *
from pygamescratch.sprite import Sprite


class HeroPlane(Sprite):
    def __init__(self, center_x, center_y):
        Sprite.__init__(self, "hero", center_x, center_y)
        self.set_size_to(50)
        self.max_hero_bullets = 10
        self.hp = 5
        self.immune = False
        self.switch_costume_to("hp3")
        self.regist_event(EVENT_MOUSE_LEFT, self.hero_single_fire)
        self.regist_event(EVENT_MOUSE_RIGHT, self.hero_triple_fire)
        self.regist_event(EVENT_MOUSE_MIDDLE, self.hero_add_friend)
        self.when_key_up(CALL_FRIEND_KEY, self.hero_add_friend)
        pygs.schedule(0, self.hero_single_fire, 0.15)
        pygs.schedule(0, self.hero_triple_fire, 0.2)

    def got_hit(self):
        self.immune = True
        pygs.play_sound("hit.wav")
        self.hp = self.hp - 1
        if self.hp <= 0:
            self.immune = False
            pygs.schedule(0.2, self.hero_down, None)
            self.switch_costume_to("hp0")
            pygs.text("ending_text", "游戏结束，得分：{0}".format(g.score), x=115, y=pygs.screen_center_y, size=28, color=(255, 255, 255))
            friend_planes = pygs.get_sprites_by_name("friendplane")
            hero_bullets = pygs.get_sprites_by_name("herobullet")
            for s in list(friend_planes):
                s.delete()
            for s in list(hero_bullets):
                s.delete()
            pygs.schedule(0.2, self.delete, None)
        else:
            pygs.schedule(1, self.recover, None)

    def recover(self):
        self.immune = False

    def hero_down(self):
        pygs.play_sound("boom.wav")
        self.switch_costume_to("down")

    def move_hero(self):
        x = 0
        y = 0
        x_speed = 2
        y_speed = 3
        if pygs.is_key_pressed(DIRECTION_DOWN_KEY) and pygs.is_key_pressed(DIRECTION_LEFT_KEY):
            x = -x_speed
            y = y_speed
        elif pygs.is_key_pressed(DIRECTION_DOWN_KEY) and pygs.is_key_pressed(DIRECTION_RIGHT_KEY):
            x = x_speed
            y = y_speed
        elif pygs.is_key_pressed(DIRECTION_UP_KEY) and pygs.is_key_pressed(DIRECTION_LEFT_KEY):
            x = -x_speed
            y = -y_speed
        elif pygs.is_key_pressed(DIRECTION_UP_KEY) and pygs.is_key_pressed(DIRECTION_RIGHT_KEY):
            x = x_speed
            y = -y_speed
        elif pygs.is_key_pressed(DIRECTION_DOWN_KEY):
            y = y_speed
        elif pygs.is_key_pressed(DIRECTION_UP_KEY):
            y = -y_speed
        elif pygs.is_key_pressed(DIRECTION_LEFT_KEY):
            x = -x_speed - 1
        elif pygs.is_key_pressed(DIRECTION_RIGHT_KEY):
            x = x_speed + 1
        self.change_x_by(x)
        self.change_y_by(y)

    def _get_fire_target_position(self, fire_key, pressed_mouse_key_index):
        if self.hp > 0:
            if pygs.is_key_pressed(fire_key):
                # 自动瞄准最近敌人
                closest_enemy = self.get_closest_sprite(g.get_enemies())
                if closest_enemy:
                    return closest_enemy.rect.center
            elif pygame.mouse.get_pressed()[pressed_mouse_key_index]:
                return pygs.mouse_position
        return None

    def hero_single_fire(self):
        target_position = self._get_fire_target_position(FIRE_SINGLE_KEY, 0)
        if target_position is not None:
            midtop = self.rect.midtop
            self._hero_fire(midtop[0], midtop[1], target_position[0], target_position[1])

    def hero_triple_fire(self):
        target_position = self._get_fire_target_position(FIRE_TRIPLE_KEY, 2)
        if target_position is not None:
            rect = self.rect
            self._hero_fire(rect.midtop[0], rect.midtop[1], target_position[0], target_position[1])
            self._hero_fire(rect.midleft[0], rect.midleft[1], target_position[0] - rect.width / 2, target_position[1])
            self._hero_fire(rect.midright[0], rect.midright[1], target_position[0] + rect.width / 2, target_position[1])

    def _hero_fire(self, x, y, target_x, target_y):
        hero_bullets = g.get_hero_bullets()
        if len(hero_bullets) >= self.max_hero_bullets:
            return
        pygs.play_sound("hero_fire.wav")
        hero_bullet = HeroBullet(x, y, BULLET_TYPE_HERO)
        hero_bullet.point_to(target_x, target_y)
        hero_bullet.switch_costume_to("bullet")



    def add_hp(self):
        if self.hp < g.max_hp:
            self.hp = self.hp + 1

    def add_bullets(self):
        if self.max_hero_bullets < g.max_bullets:
            self.max_hero_bullets = self.max_hero_bullets + 1

    def hero_add_friend(self):
        if pygs.game_paused or self.hp < 5:
            return
        x = random.randrange(0, pygs.max_x)
        y = pygs.max_y - 25
        FriendPlane(x, y)
        self.hp = self.hp - 3

    def action(self):
        self.move_hero()
        enemy_bullets = self.get_touching_sprite("enemybullet")
        for enemy_bullet in enemy_bullets:
            if enemy_bullet and not enemy_bullet.hit() and not self.immune:
                enemy_bullet.hit_plane()
                self.got_hit()
        if self.hp >= 4:
            self.switch_costume_to("hp4")
        elif self.hp > 0:
            self.switch_costume_to("hp{0}".format(self.hp))
        if self.immune:
            self.showing = not self.showing
        else:
            self.show()
        g.display_hero_bullet_score()
        g.display_hero_hp()

from friend_plane import *


class HeroPlane(Sprite):
    def __init__(self):
        Sprite.__init__(self, "hero", x=0, y=50)
        self.max_hero_bullets = 10
        self.hp = 5
        self.immune = False
        self.switch_costume_to("hp3")
        self.regist_event(EVENT_MOUSE_LEFT, self.hero_single_fire)
        self.regist_event(EVENT_MOUSE_RIGHT, self.hero_triple_fire)
        self.regist_event(EVENT_MOUSE_MIDDLE, self.hero_add_friend)
        self.when_key_up(g.CALL_FRIEND_KEY, self.hero_add_friend)
        schedule(0, self.hero_single_fire, 0.15)
        schedule(0, self.hero_triple_fire, 0.25)
        self.set_size_to(50)

    def got_hit(self):
        self.immune = True
        pygs.play_sound("hit.wav")
        self.hp = self.hp - 1
        if self.hp <= 0:
            self.immune = False
            schedule(0.2, self.hero_down, None)
            self.switch_costume_to("hp0")
            text("ending_text", "游戏结束，得分：{0}".format(g.score), x=-115, y=0, size=28, color=(255, 255, 255))
            friend_planes = get_sprites_by_name("friendplane")
            hero_bullets = get_sprites_by_name("herobullet")
            for s in list(friend_planes):
                s.delete()
            for s in list(hero_bullets):
                s.delete()
            schedule(0.2, self.delete, None)
        else:
            schedule(1, self.recover, None)

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
        if is_key_pressed(g.DIRECTION_DOWN_KEY) and is_key_pressed(g.DIRECTION_LEFT_KEY):
            x = -x_speed
            y = -y_speed
        elif is_key_pressed(g.DIRECTION_DOWN_KEY) and is_key_pressed(g.DIRECTION_RIGHT_KEY):
            x = x_speed
            y = -y_speed
        elif is_key_pressed(g.DIRECTION_UP_KEY) and is_key_pressed(g.DIRECTION_LEFT_KEY):
            x = -x_speed
            y = y_speed
        elif is_key_pressed(g.DIRECTION_UP_KEY) and is_key_pressed(g.DIRECTION_RIGHT_KEY):
            x = x_speed
            y = y_speed
        elif is_key_pressed(g.DIRECTION_DOWN_KEY):
            y = -y_speed
        elif is_key_pressed(g.DIRECTION_UP_KEY):
            y = y_speed
        elif is_key_pressed(g.DIRECTION_LEFT_KEY):
            x = -y_speed - 1
        elif is_key_pressed(g.DIRECTION_RIGHT_KEY):
            x = y_speed + 1
        self.change_x_by(x)
        self.change_y_by(y)

    def _get_fire_target_position(self, fire_key, pressed_mouse_key_index):
        if self.hp > 0:
            if is_key_pressed(fire_key):
                # 自动瞄准最近敌人
                closest_enemy = self.get_closest_sprite(g.get_enemies())
                if closest_enemy:
                    return closest_enemy.rect.center
            elif pygame.mouse.get_pressed()[pressed_mouse_key_index]:
                return pygs.mouse_position
        return None

    def hero_single_fire(self):
        target_position = self._get_fire_target_position(g.FIRE_SINGLE_KEY, 0)
        if target_position is not None:
            rect = self.rect
            self._hero_fire(rect.midleft[0], rect.midleft[1], target_position[0], target_position[1])

    def hero_triple_fire(self):
        target_position = self._get_fire_target_position(g.FIRE_TRIPLE_KEY, 2)
        if target_position is not None:
            rect = self.rect
            self._hero_fire(rect.midleft[0], rect.midleft[1], target_position[0], target_position[1])
            self._hero_fire(rect.midtop[0], rect.midtop[1], target_position[0] + rect.width / 2, target_position[1])
            self._hero_fire(rect.midtop[0] - rect.width, rect.midtop[1], target_position[0] - rect.width / 2, target_position[1])

    def _hero_fire(self, x, y, target_x, target_y):
        bullets = get_sprites_by_name("herobullet")
        if len(bullets) >= self.max_hero_bullets:
            return
        pygs.play_sound("hero_fire.wav")
        hero_bullet = HeroBullet(x, y)
        hero_bullet.point_to(target_x, target_y)
        hero_bullet.switch_costume_to("bullet")

    def add_hp(self):
        if self.hp < g.max_hp:
            self.hp = self.hp + 1

    def add_bullets(self):
        if self.max_hero_bullets < g.max_bullets:
            self.max_hero_bullets = self.max_hero_bullets + 1

    def hero_add_friend(self):
        if game_paused or self.hp < 5:
            return
        x = random.randrange(-pygs.max_x, pygs.max_x)
        y = -pygs.max_y + 25
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
        self._display_hero_bullet_score(pygs.max_x, pygs.max_y)
        self._display_hero_hp(pygs.max_x, pygs.max_y)

    def _display_hero_hp(self, max_x, max_y):
        # 显示血条
        hp_sprites = get_sprites_by_name("hp")
        if len(hp_sprites) <= 0:
            x = -max_x + 10
            for index in range(0, g.max_hp + 1):
                Sprite("hp", x + index * 25, -max_y + 50)
            hp_sprites = get_sprites_by_name("hp")
        for index in range(1, len(hp_sprites) + 1):
            hp_sprites[index - 1].showing = (index <= self.hp)

    def _display_hero_bullet_score(self, max_x, max_y):
        display_text = "分数：{0}".format(g.score)
        text("score_text", display_text, x=max_x - 110, y=-max_y + 30, size=22, color=(128, 128, 128))
        remaining_bullets = self.max_hero_bullets - len(get_sprites_by_name("herobullet"))
        text("bullet_text", "弹药：{0}".format(remaining_bullets), x=-max_x + 5, y=-max_y + 30, size=18, color=(0, 0, 0))

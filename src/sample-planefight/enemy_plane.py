from enemy_bullet import *
from supply import *


class EnemyPlane(Sprite):
    def __init__(self, enemy_type, center_x, center_y):
        Sprite.__init__(self, "enemy" + str(enemy_type), center_x, center_y)
        self.hp = g.enemy_hp_rate * (enemy_type + 1) * 2
        self.enemy_type = enemy_type
        pygs.schedule(3, self.change_direction, None)
        pygs.schedule(g.enemy_fire_wait, self.fire, g.enemy_fire_wait)

    def enemy_down(self):
        pygs.play_sound("boom.wav")
        self.switch_costume_to("down")
        g.score = g.score + self.enemy_type + 1
        if g.enemy_fire_wait > 0.05:
            g.enemy_fire_wait = g.enemy_initial_fire_wait - g.score / 300
        if g.enemy_new_wait > 0.05:
            g.enemy_new_wait = g.enemy_initial_new_wait - g.score * 2 / 100
        if self.enemy_type == 1:
            Supply("bullet", self.center_x, self.center_y)
        elif self.enemy_type == 2:
            Supply("health", self.center_x, self.center_y)
        pygs.schedule(0.2, self.delete, None)

    def action(self):
        if self.hp <= 0:
            return
        self.move(1)
        self.bounce_if_on_edge()
        hero_bullets = self.get_touching_sprite("herobullet")
        for hero_bullet in hero_bullets:
            if hero_bullet and not hero_bullet.hit():
                pygs.play_sound("herohit.wav")
                if self.hp > 0:
                    self.hp = self.hp - 1
                hero_bullet.hit_plane()
                if self.hp <= 0:
                    if self.enemy_type == 0:
                        g.enemy0_down_count = g.enemy0_down_count + 1
                    pygs.schedule(0.2, self.enemy_down, None)
        self.switch_costume_to("hp" + str(int((self.hp + (g.enemy_hp_rate - 1)) / g.enemy_hp_rate)))
        self.say(str(self.hp), 11, (143, 73, 0))

    def change_direction(self):
        self.point_to(random.randrange(-pygs.max_x, pygs.max_x), random.randrange(-pygs.max_y, pygs.max_y))

    def fire(self):
        if self.hp <= 0:
            return

        if not g.hero:
            return
        friend_planes = pygs.get_sprites_by_name("friendplane")
        # target_planes = [] + friend_planes
        target_planes = [] + friend_planes + [g.hero]
        if len(target_planes) <= 0:
            return
        randint = random.randint(0, len(target_planes) - 1)
        target_position = target_planes[randint].rect.center
        pygs.play_sound("enemy_fire.wav")
        start_middle = self.rect.midbottom
        start_right = self.rect.midright
        if not self.enemy_type == 1:
            EnemyBullet(start_middle[0], start_middle[1], target_position[0], target_position[1], self.enemy_type)
        if not self.enemy_type == 0:
            EnemyBullet(start_right[0], start_right[1] + 10, target_position[0], target_position[1], self.enemy_type)
            EnemyBullet(start_right[0] - self.rect.width, start_right[1] + 10, target_position[0], target_position[1], self.enemy_type)


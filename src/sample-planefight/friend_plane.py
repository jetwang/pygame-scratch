import global_var as g
from hero_bullet import HeroBullet
from pygamescratch import *


class FriendPlane(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self, "friendplane", x, y)
        self.hp = 10
        self.set_size_to(60)
        self.switch_costume_to("a")
        self.immune = False
        self.move_speed = 3
        pygs.play_sound("callfriend.wav")
        schedule(g.friend_change_direction_wait, self.change_direction, None)
        schedule(g.friend_fire_wait, self.friend_fire, None)

    def friend_fire(self):
        if g.hero is None:
            return
        if self.hp <= 0:
            return
        if self.showing:
            enemy_planes = g.get_enemies()
            if len(enemy_planes) > 0:
                target_position = enemy_planes[0].rect.center
                pygs.play_sound("hero_fire.wav")
                self.single_fire(self.rect.midleft, target_position)
        schedule(g.friend_fire_wait, self.friend_fire, None)

    def single_fire(self, start_position, target_position):
        hero_bullet = HeroBullet(start_position[0], start_position[1])
        hero_bullet.point_to(target_position[0], target_position[1])

    def friend_down(self):
        pygs.play_sound("boom.wav")
        self.switch_costume_to("down")
        schedule(0.2, self.delete, None)

    def got_hit(self):
        self.immune = True
        pygs.play_sound("hit.wav")
        self.hp = self.hp - 1
        if self.hp <= 0:
            schedule(0.2, self.friend_down, None)
            self.switch_costume_to("hp0")
        else:
            schedule(1, self.recover, None)

    def recover(self):
        self.immune = False

    def action(self):
        if self.hp <= 0:
            return
        self.move(self.move_speed)
        self.bounce_if_on_edge()
        enemy_bullets = self.get_touching_sprite("enemybullet")
        for enemy_bullet in enemy_bullets:
            if enemy_bullet and not enemy_bullet.hit() and not self.immune:
                enemy_bullet.hit_plane()
                self.got_hit()
        self.say(str(self.hp), 11, (51, 173, 255))
        if self.immune:
            self.showing = not self.showing
        else:
            self.show()

    def change_direction(self):
        if self.hp <= 0:
            return
        closest_enemy_bullet = self.get_closest_sprite_by_name("enemybullet")
        if closest_enemy_bullet:
            distance = get_distance(closest_enemy_bullet.rect.center, self.rect.center)
            if distance <= 100:
                if closest_enemy_bullet.rect.x >= self.rect.x:  # 如果子弹在右边
                    if self.rect.x > -pygs.max_x / 2:  # 如果友机左边还有余地
                        self.point(270)
                    else:
                        self.point(90)
                elif closest_enemy_bullet.rect.x <= self.rect.x:  # 如果子弹在左边
                    if self.rect.x < pygs.max_x / 2:  # 如果友机右边还有余地
                        self.point(90)
                    else:
                        self.point(270)
        schedule(g.friend_change_direction_wait, self.change_direction, None)

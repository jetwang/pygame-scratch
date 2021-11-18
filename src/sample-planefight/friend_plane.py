from global_var import *
from hero_bullet import HeroBullet
from pygamescratch import *
from pygamescratch.sprite import Sprite


class FriendPlane(Sprite):
    def __init__(self, center_x, center_y):
        Sprite.__init__(self, "friendplane", center_x, center_y)
        self.hp = 10
        self.set_size_to(60)
        self.switch_costume_to("a")
        self.immune = False
        self.move_speed = 3
        pygs.play_sound("callfriend.wav")
        pygs.schedule(g.friend_change_direction_wait, self.change_direction, None)
        pygs.schedule(g.friend_fire_wait, self.friend_fire, None)

    def friend_fire(self):
        if g.hero is None or g.hero.hp <= 0:
            return
        if self.hp <= 0:
            return
        if self.showing:
            enemy_planes = g.get_enemies()
            if len(enemy_planes) > 0:
                target_position = enemy_planes[0].rect.center
                pygs.play_sound("hero_fire.wav")
                self.single_fire(self.rect.midtop, target_position)
        pygs.schedule(g.friend_fire_wait, self.friend_fire, None)

    def single_fire(self, start_position, target_position):
        hero_bullet = HeroBullet(start_position[0], start_position[1])
        hero_bullet.point_to(target_position[0], target_position[1])

    def friend_down(self):
        pygs.play_sound("boom.wav")
        self.switch_costume_to("down")
        pygs.schedule(0.2, self.delete, None)

    def got_hit(self):
        self.immune = True
        pygs.play_sound("hit.wav")
        self.hp = self.hp - 1
        if self.hp <= 0:
            pygs.schedule(0.2, self.friend_down, None)
            self.switch_costume_to("hp0")
        else:
            pygs.schedule(1, self.recover, None)

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
            distance = pygs.get_distance(closest_enemy_bullet.rect.center, (self.center_x, self.center_y))
            if distance <= 100:
                if closest_enemy_bullet.center_x >= self.center_x:  # 如果子弹在右边
                    if self.rect.x > pygs.max_x / 4:  # 如果友机左边还有余地
                        self.point(180)
                    else:
                        self.point(0)
                elif closest_enemy_bullet.center_x <= self.center_x:  # 如果子弹在左边
                    if self.rect.x < pygs.max_x / 4:  # 如果友机右边还有余地
                        self.point(0)
                    else:
                        self.point(180)
        pygs.schedule(g.friend_change_direction_wait, self.change_direction, None)

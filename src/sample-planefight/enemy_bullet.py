from pygamescratch import *


class EnemyBullet(Sprite):
    def __init__(self, center_x, center_y, target_x, target_y, enemy_type):
        Sprite.__init__(self, "enemybullet", center_x, center_y)
        if enemy_type == 0:
            self.set_size_to(50)
            self.switch_costume_to("bullet1")
            self.move_speed = 2
        elif enemy_type == 1:
            self.set_size_to(80)
            self.move_speed = 2
        elif enemy_type == 2:
            self.set_size_to(80)
            self.move_speed = 2
        self.point_to(target_x, target_y)
        self.rotate_angle = 90 - self.direction

    def action(self):
        if self.showing and not self.hit():
            self.move(self.move_speed)
            if self.touching_edge():
                self.delete()

    def hit_plane(self):
        self.switch_costume_to("hit")
        pygs.schedule(0.2, self.delete, None)

    def hit(self):
        return self.current_costume_key == "hit"

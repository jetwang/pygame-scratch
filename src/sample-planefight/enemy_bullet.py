from pygamescratch import *


class EnemyBullet(Sprite):
    def __init__(self, x, y, target_x, target_y):
        Sprite.__init__(self, "enemybullet", x, y)
        self.move_speed = 3
        self.point_to(target_x, target_y)
        self.set_size_to(50)

    def action(self):
        if self.showing and not self.hit():
            self.move(self.move_speed)
            if self.touching_edge():
                self.delete()

    def hit_plane(self):
        self.switch_costume_to("hit")
        schedule(0.2, self.delete, None)

    def hit(self):
        return self.current_costume_key == "hit"

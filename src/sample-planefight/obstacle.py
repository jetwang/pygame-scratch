from pygamescratch.sprite import Sprite


class Obstacle(Sprite):
    def __init__(self, center_x, center_y):
        Sprite.__init__(self, "obstacle", center_x, center_y)
        self.set_size_to(60)

    def action(self):
        bullets = self.get_touching_sprite("enemybullet")
        bullets.extend(self.get_touching_sprite("herobullet"))
        for bullet in bullets:
            bullet.hit_plane()

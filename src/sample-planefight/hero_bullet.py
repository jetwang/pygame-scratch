from global_var import *


class HeroBullet(Sprite):
    def __init__(self, center_x, center_y, bullet_type, target_sprite=None):
        Sprite.__init__(self, "herobullet", center_x, center_y)
        self.bullet_type = bullet_type
        self.target_sprite = target_sprite
        if bullet_type == BULLET_TYPE_HERO:
            self.set_size_to(50)
        else:
            self.set_size_to(35)

    def action(self):
        if self.showing and not self.hit():
            if self.bullet_type == BULLET_TYPE_HERO:
                self.move(7 + g.max_bullets / 10)
            else:
                if self.target_sprite and self.target_sprite.hp > 0:
                    self.point_to(self.target_sprite.center_x, self.target_sprite.center_y)
                self.move(8)
            if self.touching_edge():
                self.delete()

    def hit_plane(self):
        self.switch_costume_to("hit")
        pygs.schedule(0.2, self.delete, None)

    def hit(self):
        return self.current_costume_key == "hit"

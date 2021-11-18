from pygamescratch import *


class HeroBullet(Sprite):
    def __init__(self, center_x, center_y):
        Sprite.__init__(self, "herobullet", center_x, center_y)
        self.set_size_to(50)

    def action(self):
        if self.showing and not self.hit():
            self.move(7)
            if self.touching_edge():
                self.delete()

    def hit_plane(self):
        self.switch_costume_to("hit")
        pygs.schedule(0.2, self.delete, None)

    def hit(self):
        return self.current_costume_key == "hit"

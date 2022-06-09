import random

from pygamescratch import Sprite, pygs


class WBC(Sprite):

    def __init__(self, sprite_name, center_x=pygs.max_x, center_y=pygs.max_y):
        super().__init__(sprite_name, center_x, center_y)
        self.point(random.randint(-90, 180))
        pygs.schedule(25, self.delete, None)
        self.acting_size_changes = 0.5

    def action(self):
        self.move(3)
        self.bounce_if_on_edge()
        if self.size <= 85 or self.size >= 100:
            self.acting_size_changes = -self.acting_size_changes
        self.set_size_to(self.size + self.acting_size_changes)


import random

from WBC import WBC
from pygamescratch import Sprite, pygs


class WBCBag(Sprite):
    def __init__(self, center_x=0, center_y=0):
        super().__init__("wbc_bag", center_x, center_y)
        self.m = 1
        self.point(random.randint(-90, 270))
        self.got = False

    def action(self):
        self.move(self.m)
        if self.touching_edge():
            self.point(random.randint(-90, 270))
        if self.get_touching_sprite("robot"):
            pygs.play_sound("泡泡弹出.wav")
            WBC("WBC", self.center_x, self.center_y)
            self.delete()

import random

from pygamescratch import Sprite, pygs
from store import Store


class RescueBag(Sprite):
    def __init__(self, center_x=0, center_y=0):
        super().__init__("rescue_bag", center_x, center_y)
        self.m = 1
        self.point(random.randint(-90, 270))
        self.got = False

    def action(self):
        self.move(self.m)
        if self.touching_edge():
            if self.got:
                self.delete()
            else:
                self.point(random.randint(-90, 270))
        if not self.got:
            good = self.get_touching_sprite("robot")
            if len(good) > 0:
                pygs.play_sound("能量棒补给.wav")
                self.point_to(0, pygs.max_y)
                self.m = 8
                Store.human_body.hp += 500
                self.got = True

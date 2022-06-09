from pygamescratch import Sprite, pygs

from store import Store


class PillBag(Sprite):

    def __init__(self, center_x=0, center_y=0):
        super().__init__("pillbag", center_x, center_y)
        self.point(90)
        self.m = 1
        self.got = False

    def action(self):
        self.move(self.m)
        if self.touching_edge():
            self.delete()
        if not self.got:
            if self.get_touching_sprite("robot"):
                self.got = True
                pygs.play_sound("能量棒补给.wav")
                self.point_to_sprite(Store.tby)
                self.m = 10
                Store.robot.pills += 1

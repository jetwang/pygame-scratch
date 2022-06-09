from WBC import WBC
from pygamescratch import Sprite, pygs


class WBCBag(Sprite):

    def action(self):
        self.y = self.center_y
        self.y_speed = 1
        self.y = self.y_speed
        self.change_y_by(self.y)
        if self.touching_edge():
            self.delete()
        if self.get_touching_sprite("robot"):
            pygs.play_sound("泡泡弹出.wav")
            WBC("WBC", self.center_x, self.center_y)
            self.delete()

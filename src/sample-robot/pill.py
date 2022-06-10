from pygamescratch import Sprite, pygs


class Pill(Sprite):

    def __init__(self, sprite_name, center_x=0, center_y=0):
        super().__init__(sprite_name, center_x, center_y)
        pygs.schedule(10, self.delete, None)

    def action(self):
        self.change_x_by(3)

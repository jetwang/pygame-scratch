from pygamescratch import Sprite, pygs
from store import Store



class Pill(Sprite):

    def __init__(self, sprite_name, center_x=0, center_y=0):
        super().__init__(sprite_name, center_x, center_y)
        pygs.schedule(10,self.delete,0)


    def action(self):
        if not self.center_y >= Store.human_body.center_y:
            self.change_x_by(-8)



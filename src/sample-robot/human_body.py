from pygamescratch import Sprite, pygs
from store import Store


class HumanBody(Sprite):

    def __init__(self, sprite_name, center_x=0, center_y=0):
        super().__init__(sprite_name, center_x, center_y)
        self.hp = Store.max_hp
        self.hitting = False

    def action(self):
        virus = self.get_touching_sprite("virus1")
        virus.extend(self.get_touching_sprite("virus2"))
        virus.extend(self.get_touching_sprite("virus3"))
        if len(virus) > 0:
            pygs.play_sound("吃东西.wav")
            self.hitting = True
            pygs.schedule(1, self.recover, None)
            if not virus[0].is_dead():
                self.hp -= virus[0].hurt
                virus[0].delete()
        if self.hp > Store.max_hp:
            self.hp = Store.max_hp
        if self.hitting:
            self.showing = not self.showing
        else:
            self.show()

    def recover(self):
        self.hitting = False

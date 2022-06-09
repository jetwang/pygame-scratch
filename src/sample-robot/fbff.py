from pygamescratch import Sprite

from store import Store


class Fbff(Sprite):
    def action(self):
        self.hide()
        self.say(str(Store.robot.pills)+"/80")

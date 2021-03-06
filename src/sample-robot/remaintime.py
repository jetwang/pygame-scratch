import random

from pillbag import PillBag
from pygamescratch import pygs
from rescuebag import RescueBag
from store import Store
from wbc_bag import WBCBag


class RemainTime:

    def __init__(self):
        self.timeo = 120
        pygs.schedule(1, self.time, 1)
        pygs.schedule(10, self.create_pill_bag, 8)
        pygs.schedule(20, self.creat_wbc_bags, 8)
        pygs.schedule(30, self.creat_rescue_bag, 10)

    def create_pill_bag(self):
        PillBag(random.randint(0, pygs.max_x), 20)

    def creat_rescue_bag(self):
        if Store.human_body.hp < Store.max_hp:
            RescueBag(random.randint(0, pygs.max_x), 20)

    def creat_wbc_bags(self):
        WBCBag(random.randint(0, pygs.max_x), 20)

    def time(self):
        self.timeo = self.timeo - 1
        pygs.text("f", str(Store.human_body.hp), x=50, y=pygs.max_y-100, size=16, color=(0, 0, 0))
        pygs.text("pilles", str(Store.robot.pills),x=50, y=pygs.max_y-70, size=16, color=(0, 0, 0))
        pygs.text("schedule_time", str(self.timeo), x=50, y=pygs.max_y-40, size=16, color=(0, 0, 0))

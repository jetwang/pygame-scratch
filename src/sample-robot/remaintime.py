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
        PillBag(random.randint(0, pygs.max_x), 10)

    def creat_rescue_bag(self):
        if Store.human_body.hp < 3000:
            RescueBag(random.randint(0, pygs.max_y), 10)

    def creat_wbc_bags(self):
        WBCBag("wbc_bag", random.randint(0, pygs.max_x), 10)

    def time(self):
        self.timeo = self.timeo - 1
        pygs.text("f", str(Store.human_body.hp), x=pygs.max_x - 60, y=20, size=16, color=(0, 0, 0))
        pygs.text("pilles", str(Store.robot.pills), x=pygs.max_x - 60, y=50, size=16, color=(0, 0, 0))
        pygs.text("schedule_time", str(self.timeo), x=pygs.max_x - 60, y=80, size=16, color=(0, 0, 0))

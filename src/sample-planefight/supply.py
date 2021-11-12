from pygamescratch import *
import global_var as g


class Supply(Sprite):
    def __init__(self, supply_type, x, y):
        Sprite.__init__(self, "supply", x, y)
        self.got = False
        self.point(180)
        self.set_size_to(60)
        self.switch_costume_to(supply_type + "_supply")
        self.supply_type = supply_type

    def action(self):
        if self.showing:
            if self.got:
                self.point_to(-pygs.max_x, -pygs.max_y)
                self.move(8)
            else:
                self.move(1)
            if self.touching_edge():
                self.delete()
            if self.got:
                return
            touching_hero_planes = self.get_touching_sprite("hero")
            touching_friend_planes = self.get_touching_sprite("friendplane")
            if g.hero and (len(touching_hero_planes) > 0 or len(touching_friend_planes) > 0):
                pygs.play_sound("supply.ogg")
                if "health" == self.supply_type:
                    g.hero.add_hp()
                elif "bullet" == self.supply_type:
                    g.hero.add_bullets()
                self.got = True

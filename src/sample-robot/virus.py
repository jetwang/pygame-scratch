from enum import Enum

from pygamescratch import Sprite, pygs
from store import Store


class VirusStatus(Enum):
    normal = 0
    hitting = 1
    dead = 3


class Virus(Sprite):

    def __init__(self, virus_type, center_x=0, center_y=0):
        super().__init__("virus" + str(virus_type), center_x, center_y)
        self.status = VirusStatus.normal
        self.hp = 2
        self.acting_size_changes = 0.5
        self.hurt = 500 - virus_type * 100
        self.speed = virus_type
        self.virus_name = ['阿尔法', '德尔塔', '奥密克戎'][virus_type - 1]
        self.clock_tip = 0

    def action(self):
        self.clock_tip += 1
        if self.status == VirusStatus.dead:
            self.show()
            self.say("")
            self.point(-45)
            self.move(3)
            new_size = self.size - 3
            if new_size > 0:
                self.set_size_to(new_size)
            else:
                self.delete()
                return
        elif self.status == VirusStatus.hitting:
            self.point(0)
            if not self.touching_edge():
                self.move(5)
            self.breath()
            self.showing = self.clock_tip % 3 != 1
        elif self.status == VirusStatus.normal:
            self.show()
            self.point(180)
            self.say(self.virus_name, 14, (80, 80, 80))
            self.move(self.speed)
            self.breath()
            hitting_sprites = self.get_touching_sprite("robot")
            if len(hitting_sprites) > 0:
                Store.robot.attack()
                self.got_hit()
            else:
                hitting_sprites.extend(self.get_touching_sprite("pill"))
                hitting_sprites.extend(self.get_touching_sprite("WBC"))
                if len(hitting_sprites) > 0:
                    self.got_hit()

    def breath(self):
        if self.size <= 85 or self.size >= 100:
            self.acting_size_changes = -self.acting_size_changes
        self.set_size_to(self.size + self.acting_size_changes)

    def got_hit(self):
        self.hp -= 1
        if self.hp > 0:
            pygs.play_sound("击打身体.wav")
            self.status = VirusStatus.hitting
            pygs.schedule(1, self.recover, None)
        else:
            pygs.play_sound("破碎.wav")
            self.status = VirusStatus.dead

    def is_dead(self):
        return self.status == VirusStatus.dead

    def recover(self):
        self.status = VirusStatus.normal

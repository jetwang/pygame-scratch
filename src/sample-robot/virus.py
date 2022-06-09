from pygamescratch import Sprite, pygs


class Virus(Sprite):

    def __init__(self, virus_type, center_x=0, center_y=0):
        super().__init__("virus" + str(virus_type), center_x, center_y)
        self.died = False
        self.point(90)
        self.acting_size_changes = 0.5
        self.hurt = 500 - virus_type * 100
        self.speed = virus_type
        self.virus_name = ['阿尔法', '德尔塔', '奥密克戎'][virus_type - 1]

    def action(self):
        if self.died:
            self.say("")
            self.point(-90)
            self.move(3)
            new_size = self.size - 3
            if new_size > 0:
                self.set_size_to(new_size)
            else:
                self.delete()
                return
        else:
            self.say(self.virus_name, 14, (80, 80, 80))
            self.move(self.speed)
            if self.size <= 85 or self.size >= 100:
                self.acting_size_changes = -self.acting_size_changes
            self.set_size_to(self.size + self.acting_size_changes)
            hitting_sprites = self.get_touching_sprite("robot")
            hitting_sprites.extend(self.get_touching_sprite("pill"))
            hitting_sprites.extend(self.get_touching_sprite("WBC"))
            if len(hitting_sprites)>0:
                pygs.play_sound("击打身体.wav")
                self.died = True
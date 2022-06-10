from pygame import K_w, K_s, K_a, K_d, K_j

from pill import Pill
from pygamescratch import Sprite, pygs
from store import Store


class Robot(Sprite):

    def __init__(self, sprite_name, center_x=0, center_y=0):
        super().__init__(sprite_name, center_x, center_y)
        self.pills = 0
        self.target = None
        pygs.when_key_up(K_j, self.fire_current)
        from pygamescratch import EVENT_MOUSE_LEFT
        self.regist_event(EVENT_MOUSE_LEFT, self.fire_mouse)
        self.goto_front_layer()
        self.attacking = False

    def action(self):
        x = 0
        y = 0
        self.x_speed = 10
        self.y_speed = 10
        if pygs.is_key_pressed(K_w):
            y = -self.y_speed
        if pygs.is_key_pressed(K_s):
            y = self.y_speed
        if pygs.is_key_pressed(K_a):
            x = -self.x_speed
        if pygs.is_key_pressed(K_d):
            x = self.x_speed
        if self.pills > 80:
            self.pills = 80
        if x != 0 or y != 0:
            self.walking()
        self.change_x_by(x)
        self.change_y_by(y)
        if Store.timeo.timeo <= 0 < Store.human_body.hp:
            pygs.text("score_texta", "恭喜你，成功拯救了病人！", x=pygs.screen_center_x - 140, y=pygs.screen_center_y - 60, size=22)
            pygs.text("score_textb", "               ", x=pygs.screen_center_x - 140, y=pygs.screen_center_y - 40, size=22)
            pygs.text("score_textc", "重启游戏请按回车键", x=pygs.screen_center_x - 140, y=pygs.screen_center_y - 20, size=22)
            pygs.clear_schedule()
            pygs.clear_sprites()

        elif Store.human_body.hp <= 0:
            pygs.text("score_textd", "你失败了，继续加油吧！", x=pygs.screen_center_x - 140, y=pygs.screen_center_y - 60, size=22)
            pygs.text("score_texte", "                  ", x=pygs.screen_center_x - 140, y=pygs.screen_center_y - 40,
                      size=22)
            pygs.text("store_testf", "重启游戏请按回车键", x=pygs.screen_center_x - 140, y=pygs.screen_center_y - 20, size=22)
            pygs.clear_sprites()
            pygs.clear_schedule()

    def fire_current(self):
        self.target = (self.center_x, self.center_y)
        self.fire()

    def fire_mouse(self):
        self.target = (self.center_x, self.center_y)
        # self.target = pygs.mouse_position
        self.fire()

    def walking(self):
        pass

    def attack(self):
        self.attacking = True
        self.switch_costume_to("2")
        pygs.schedule(0.5, self.recover, None)

    def fire(self):
        if self.target is not None and self.pills > 0:
            pygs.play_sound("biu.wav")
            self.pills -= 1
            pill = Pill("pill", self.target[0], self.target[1])
            pill.set_size_to(80)
            self.target = None

    def recover(self):
        self.attacking = False
        self.switch_costume_to("0")

from pygame.color import THECOLORS

from pygamescratch import *


class Cat(Sprite):
    def action(self):
        self.move(1)
        balls = self.get_touching_sprite("ball")
        if len(balls) > 0:
            ball = balls[0]
            ball.delete()


def start_up():
    ball = Sprite("ball", 300, 200)
    cat = Cat("cat", 5, 200)
    cat.point_to(ball.rect.center[0], ball.rect.center[1])


if __name__ == "__main__":
    pygs.default_screen_size = [1000, 500]
    pygs.default_backdrop_color = THECOLORS["white"]
    regist_global_event(EVENT_START, start_up)
    start()

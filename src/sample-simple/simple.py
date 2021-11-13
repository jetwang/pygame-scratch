from pygame.color import THECOLORS

from pygamescratch import *


class Cat(Sprite):
    def action(self):
        self.move(1)
        print(self.rect)
        print(pygame_rect(self.rect))
        balls = self.get_touching_sprite("ball")
        if len(balls) > 0:
            ball = balls[0]
            ball.delete()


def start_up():
    ball = Sprite("ball", 300, 200)
    cat = Cat("cat", 0, 0)
    cat.point_to_sprite(ball)


if __name__ == "__main__":
    pygs.screen_size(1000, 500)
    pygs.default_backdrop_color = THECOLORS["white"]
    regist_global_event(EVENT_START, start_up)
    start()

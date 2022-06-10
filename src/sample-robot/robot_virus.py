import random

import pygame
from pygame import K_SPACE, K_RETURN

from human_body import HumanBody
from pygamescratch import pygs, EVENT_START
from remaintime import RemainTime
from robot import Robot
from store import Store
from virus import Virus


def start_up():
    pygs.clear_text()
    pygs.clear_sprites()
    pygs.clear_schedule()
    Store.timeo = RemainTime()
    Store.human_body = HumanBody("human_body", -50, pygs.screen_center_y)
    from pygamescratch import Sprite
    Store.tbf = Sprite("tbf", 30, pygs.max_y-90)
    Store.tby = Sprite("tby", 30, pygs.max_y-60)
    Store.tbt = Sprite("tbt", 30, pygs.max_y-30)
    Store.tby.set_size_to(50)
    Store.tbt.set_size_to(50)
    Store.tbf.set_size_to(50)
    Store.robot = Robot("robot", 500, 400)
    pygs.schedule(2, virus1, 3)
    pygs.schedule(30, virus2, 2)
    pygs.schedule(60, virus3, 1)
    pygs.add_backdrop("images/backdrop/img.jpg")


def virus1():
    Virus(1, pygs.max_x,random.randint(0, pygs.max_y))


def virus2():
    Virus(2, pygs.max_x,random.randint(0, pygs.max_y))


def virus3():
    Virus(3, pygs.max_x,random.randint(0, pygs.max_y))


def change_game_paused_state():
    pygs.game_paused = not pygs.game_paused
    say = [
        "游戏背景：",
        "你是一个纳米机器人",
        "被医生注射到新冠患者身体里抵抗病毒",
        "科学家已经开始研发击败新冠病毒的特效药",
        "你的任务是在特效药出来之前，阻止新冠病毒攻击，保护肺",
        "          ",
        "游戏玩法:",
        "1.肺活量原始值3000，病毒攻入底下的肺部会减少肺活量，肺活量小于等于0，病人死亡",
        "2.圈圈包围住的是科学家投放的装备，分别可以增加肺活量，召唤白细胞，提供药丸",
        "3.纳米机器人上下左右移动：W、A、D、S四个键",
        "4.纳米机器人如果手中有药丸，可以点击鼠标左键投放指定位置",
        "5.开始、暂停、继续：空格",
        "6.重启游戏：回车键"
        "          ",
        "纳米机器人，别紧张,科学家们会投放一些回复肺活量的医药包的。"]
    if pygs.game_paused:
        y = 0
        for says in say:
            y = y + 20
            pygs.text("says" + str(y), says, x=20, y=y, size=18, color=(0, 0, 0))
    else:
        pygs.clear_text()


if __name__ == "__main__":
    font_name = "./font/fangzhengjianzhi.ttf"
    pygs.default_font_name = font_name
    pygs.screen_size(1100, 550)
    pygame.display.set_caption("抗疫大作战")
    pygs.regist_global_event(EVENT_START, start_up)
    pygs.background_music_load("background.wav")
    pygame.mixer.music.set_volume(1)
    pygs.regist_global_event(EVENT_START, change_game_paused_state)
    pygs.when_key_up(K_SPACE, change_game_paused_state)
    pygs.when_key_up(K_RETURN, start_up)
    pygs.start()

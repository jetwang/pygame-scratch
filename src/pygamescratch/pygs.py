# encoding: utf-8
# module pygamescratch
#
import math
import os
import random
import sys
import threading
import time
import traceback
from collections import OrderedDict

import pygame
from pygame.locals import *

# 以下是私有变量，不对外
_EVENT_KEY_UP = "_EVENT_KEY_UP"
_EVENT_KEY_DOWN = "_EVENT_KEY_DOWN"
_game_running = True  # 当前游戏是否在运行
_fps = 60  # 帧数
_time_piece = 1 / _fps  # 每帧时间间隔

_screen = None  # pygame的screen对象
_events = OrderedDict()  # 存放所有触发的事件
_global_event_watcher = {}  # 存放所有的事件监听器
_delay_functions = []  # 存放所有待延迟执行的函数
_current_backdrop = None  # 当前背景
_backdrop_key = None  # 当前背景key
_backdrops = OrderedDict()  # 存放所有背景的map
_sprites_in_game = OrderedDict()  # 存放所有角色对象
_sprites_max_id = 0  # 每创建一个角色就会赋予一个编号，该变量存放当前最大的角色编号

_texts = OrderedDict()  # 存放要显示在screen中的所有文本，文本id为主键
_key_down_list = []  # 存放当前按住的键位列表
_default_screen_size = (470, 700)  # 默认窗口大小

# 以下是默认参数，外部可以修改
default_music_folder = "./music/"  # 默认音乐文件夹
default_font_folder = "./font/"  # 默认字体文件夹
default_sprite_image_folder = "./images/sprite/"  # 默认角色文件夹
default_backdrop_image_folder = "./images/backdrop/"  # 默认字体文件夹
default_backdrop_color = (255, 255, 255)  # 默认背景色
default_font_name = None  # 默认字体名称
default_key_repeat_delay = 20  # 按压键盘重复触发key down事件的间隔
max_x, max_y = _default_screen_size
screen_center_x, screen_center_y = (max_x / 2, max_y / 2)

# 以下是默认事件名称，可以引用
EVENT_MOUSE_LEFT = "_EVENT_MOUSE_LEFT"
EVENT_MOUSE_RIGHT = "_EVENT_MOUSE_RIGHT"
EVENT_MOUSE_MIDDLE = "_EVENT_MOUSE_MIDDLE"
EVENT_START = "EVENT_START"
EVENT_SPRITE_CREATED = "_EVENT_SPRITE_CREATED"

# 以下是公共变量，可以访问
mouse_position = (0, 0)  # 存放当前鼠标的位置
game_paused = False  # 当前游戏是否暂停


def screen_size(width, height):
    """
    修改屏幕大小
    :param width:
    :param height:
    :return:
    """
    global max_x
    global max_y
    global screen_center_x
    global screen_center_y
    global _default_screen_size
    _default_screen_size = (width, height)
    max_x, max_y = _default_screen_size
    screen_center_x, screen_center_y = (max_x / 2, max_y / 2)


def text(text_id, text_str, x, y, size=40, color=(128, 128, 128)):
    """
    添加一行文字，改文字会保存到一个列表当中，每次渲染的时候都会显示
    :param text_id: 文本id
    :param text_str: 要显示的字符串
    :param x: 第一个文字的x坐标
    :param y: 第一个文字的y坐标
    :param size: 字体大小
    :param color: 字体颜色
    :return: 返回该文本对象，输入的参数都成为该对象的属性
    """
    if not isinstance(text_str, str):
        text_str = str(text_str)
    text_font = pygame.font.Font(default_font_name, size)
    text_image = text_font.render(text_str, True, color)
    new_text = {"text": text_str, "x": x, "y": y, "size": size, "image": text_image}
    _texts[text_id] = new_text
    return new_text


def remove_text(text_id):
    """
    移除文字
    :param text_id: 要移除的文字id
    :return:
    """
    if text_id:
        if text_id in _texts.keys():
            del _texts[text_id]


def clear_text():
    """
    移除所有文字
    :return:
    """
    _texts.clear()


def get_sprites_by_name(sprite_name):
    """
    根据角色名称返回角色列表
    :param sprite_name: 角色名称
    :return: 对应名称的所有角色列表
    """
    sprites = []
    for s in list(_sprites_in_game.values()):
        if s.sprite_name == sprite_name:
            sprites.append(s)
    return sprites


def refresh_events():
    """
    刷新事件列表，前一帧之前触发的事件都会被清除，不管有没有触发过
    """
    global _events
    new_events = {}
    start_time = time.perf_counter()
    for event_name, time_list in _events.items():
        new_time_list = []
        for event_time in time_list:
            if event_time > start_time - _time_piece:  # not too old
                new_time_list.append(event_time)
        if len(new_time_list) > 0:
            new_events[event_name] = new_time_list
    _events = new_events


def schedule(delay_seconds, func, repeat_interval, *args, **kwargs):
    """
    延迟执行函数
    :param delay_seconds: 等待时长
    :param func:  执行的函数对象
    :param repeat_interval: 重复执行间隔，如果为None或者不大于0，只执行一次
    :param args:  传入的无名参数
    :param kwargs:  关键字参数
    :return:
    """
    current_time = time.perf_counter()
    run_time = current_time + delay_seconds
    func_data = [run_time, func, repeat_interval, args, kwargs]
    _delay_functions.append(func_data)


def _execute_delay_functions():
    current_time = time.perf_counter()
    for func_data in list(_delay_functions):
        if func_data[0] <= current_time:
            func_data[1](*func_data[3], **func_data[4])
            if func_data[2] is not None and func_data[2] > 0:
                func_data[0] = current_time + func_data[2]
            else:
                _delay_functions.remove(func_data)


def play_sound(sound):
    """
    播放音乐
    :param sound: 音乐文件的名称（包含扩展名），函数会自动在default_music_folder定义的文件夹下面寻找对应的音乐文件
    :return:
    """
    if pygame.mixer.get_init() is None:
        pygame.mixer.init()
    sound_file = pygame.mixer.Sound(default_music_folder + sound)
    sound_file.play()


def background_music_load(music_name):
    """
    载入背景音乐
    :param music_name: 音乐文件的名称（包含扩展名），函数会自动在default_music_folder定义的文件夹下面寻找对应的音乐文件
    :return:
    """
    try:
        pygame.mixer.music.load(default_music_folder + music_name)  # 游戏背景音乐
        pygame.mixer.music.set_volume(0.6)  # 设置音量(0-1)
        pygame.mixer.music.play(-1)  # 循环播放
    except Exception as e:
        raise


def _sprites_frame_action():
    for s in list(_sprites_in_game.values()):
        if not s.sprite.get_locked():
            s.action()


def _update_screen():
    if not _game_running:
        return
    # draw back ground
    if _current_backdrop:
        _display_backdrop(_screen, _current_backdrop)
    else:
        _screen.fill(default_backdrop_color)
    # draw all sprite
    for s in list(_sprites_in_game.values()):
        if not s.sprite.get_locked() and s.showing:
            rect = s.rect
            if s.rotate_angle != 0:
                new_sprite = pygame.transform.rotate(s.sprite, s.rotate_angle)
                _screen.blit(new_sprite, rect)
            else:
                _screen.blit(s.sprite, rect)
            if s.text_end_time is not None and time.perf_counter() > s.text_end_time:
                s.text = None
                s.text_end_time = None
            if s.text:
                text_image = s.text['text_image']
                text_rect = text_image.get_rect()
                text_x = rect.x
                text_y = rect.y
                if text_x < 0:
                    text_x = rect.x + text_rect.width
                if s.text['bg_color']:
                    pygame.draw.circle(_screen, s.text['bg_color'], [text_x, text_y], text_rect.width / 2 + 2,
                                       text_rect.width + 2)
                _screen.blit(text_image, (text_x, text_y))

    for t in _texts.values():
        start_x = t['x']
        start_y = t['y']
        _screen.blit(t['image'], (start_x, start_y))

    pygame.display.update()


def _display_backdrop(screen, backdrop):
    image_ = backdrop["image"]
    if image_.get_locked():
        return
    screen.blit(image_, (backdrop["x"], backdrop["y"]))
    rect = image_.get_rect()
    if backdrop["x"] < 0 and backdrop["x"] + rect.width < max_x:
        screen.blit(image_, (backdrop["x"] + rect.width, backdrop["y"]))
    if backdrop["x"] > 0:
        screen.blit(image_, (backdrop["x"] - rect.width, backdrop["y"]))
    if backdrop["y"] < 0 and backdrop["y"] + rect.height < max_y:
        screen.blit(image_, (backdrop["x"], backdrop["y"] + rect.height))
    if backdrop["y"] > 0:
        screen.blit(image_, (backdrop["x"], backdrop["y"] - rect.height))
    backdrop["x"] = backdrop["x"] + backdrop["moving_x"]
    backdrop["y"] = backdrop["y"] + backdrop["moving_y"]
    if backdrop["x"] < -rect.width or backdrop["x"] > rect.width:
        backdrop["x"] = 0
    if backdrop["y"] < -rect.height or backdrop["y"] > rect.height:
        backdrop["y"] = 0


def _frame_loop():
    while _game_running:
        try:

            # time fragment
            start_time = time.perf_counter()
            if not game_paused:
                # event
                refresh_events()
                # events.clear()
                _execute_delay_functions()
                _sprites_frame_action()
            _update_screen()
            elapsed = time.perf_counter() - start_time

            if _time_piece > elapsed:
                time.sleep(_time_piece - elapsed)
        except Exception as e:
            print_exception(e)


def print_exception(e):
    """
    打印出异常信息
    :param e: 异常
    :return:
    """
    print('str(Exception):\t', str(Exception))
    print('str(e):\t\t', str(e))
    print('repr(e):\t', repr(e))
    # print('e.message:\t', e.message)
    print('traceback.print_exc():', traceback.print_exc())
    print('traceback.format_exc():\n%s' % traceback.format_exc())


def global_event(event_name, *args, **kwargs):
    """
    全局范围内触发事件
    :param event_name: 触发事件名称
    :param args: 要传入事件触发函数的可变参数
    :param kwargs: 要传入事件触发函数的关键字参数
    :return:
    """
    if kwargs and "event_time" in kwargs:
        event_time = kwargs["event_time"]
    else:
        event_time = time.perf_counter()
    # append event to global events
    if event_name in _events:
        _events[event_name].append(event_time)
    else:
        _events[event_name] = [event_time]

    _trigger_global_event(event_name, *args, **kwargs)
    if not game_paused:
        for s in list(_sprites_in_game.values()):
            s.event(event_name, *args, **kwargs)


def regist_global_event(event_name, func):
    """
    全局范围内注册事件监听器
    :param event_name: 监听的事件名称
    :param func: 待触发的函数
    :return:
    """
    if event_name in _global_event_watcher:
        functions = _global_event_watcher.get(event_name)
        functions.append(func)
    else:
        _global_event_watcher[event_name] = [func]


def when_key_pressed(key_name, func):
    """
    注册按键事件监听器
    :param key_name: 监听的按键值
    :param func: 待触发的函数
    :return:
    """
    regist_global_event(_get_key_down_event_name(key_name), func)


def when_key_up(key_name, func):
    """
    注册松开按键事件
    :param key_name: 监听的松开的按键值
    :param func: 待触发的函数
    :return:
    """
    regist_global_event(_get_key_up_event_name(key_name), func)


def _trigger_global_event(event_name, *args, **kwargs):
    if event_name in _global_event_watcher:
        functions = _global_event_watcher.get(event_name)
        for func in functions:
            func(*args, **kwargs)


def game_name(name):
    """
    设置游戏名称
    :param name: 游戏名称
    :return:
    """
    pygame.display.set_caption(name)


def is_key_pressed(key):
    """
    判断该键是否按住
    :param key: 要判断的按键值
    :return:
    """
    return key in _key_down_list


def get_distance(point1, point2):
    """
    获取两个坐标之间的距离
    :param point1:
    :param point2:
    :return:
    """
    return math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))


def _get_events():
    global _game_running
    global mouse_position
    pos = pygame.mouse.get_pos()
    mouse_position = (pos[0]), (pos[1])

    for event in pygame.event.get():
        if event.type == QUIT:
            _game_running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not (event.key in _key_down_list):
                _key_down_list.append(event.key)
            global_event(_get_key_down_event_name(event.key))
        if event.type == pygame.KEYUP:
            _key_down_list.remove(event.key)
            global_event(_get_key_up_event_name(event.key))
        if event.type == MOUSEBUTTONDOWN:  # 鼠标按下
            pressed_array = pygame.mouse.get_pressed()  # 获得鼠标点击类型[0,1,2] 左键,滑轮,右键
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    if index == 0:  # 点击了鼠标左键
                        global_event(EVENT_MOUSE_LEFT)
                    if index == 1:  # 点击了鼠标中键
                        global_event(EVENT_MOUSE_MIDDLE)
                    if index == 2:  # 点击了鼠标右键
                        global_event(EVENT_MOUSE_RIGHT)


def _get_key_up_event_name(key):
    return _EVENT_KEY_UP + str(key)


def _get_key_down_event_name(key):
    return _EVENT_KEY_DOWN + str(key)


def start():
    """
    开始游戏，该方法会初始化pygame，并且做两件事情，
    一是在主线程循环获取键盘和鼠标事件，并触发相应事件监听器
    二是启动一个线程，该线程会每帧重复执行：清除过期事件、执行角色活动、执行定时任务、渲染窗口，
    :return:
    """
    global _screen
    global _game_running
    pygame.init()
    _screen = pygame.display.set_mode(_default_screen_size)

    _screen.fill(default_backdrop_color)
    pygame.font.init()
    pygame.key.set_repeat(default_key_repeat_delay)

    _game_running = True
    global_event(EVENT_START)
    threading.Thread(target=_frame_loop).start()

    while _game_running:
        try:
            _get_events()
            time.sleep(0.01)
        except Exception as e:
            print_exception(e)


def add_backdrop(name, moving_x=0, moving_y=0):
    """
    增加背景
    :param name: 背景文件路径，可以传入完整路径，也可以只传入背景文件名，程序会自动到default_backdrop_image_folder定义的文件夹中找到以jpg结尾的同名的图片
    :return:
    """
    global _current_backdrop
    global _backdrop_key
    global _backdrops
    if os.path.exists(name):
        backdrop_image = pygame.image.load(name).convert_alpha()
    else:
        if not name.endswith(".jpg"):
            path = default_backdrop_image_folder + name + ".jpg"
            backdrop_image = pygame.image.load(path).convert_alpha()
    backdrop = {"x": 0, "y": 0, "image": backdrop_image, "moving_x": moving_x, "moving_y": moving_y}
    _backdrops[name] = backdrop
    _current_backdrop = backdrop
    _backdrop_key = name


def switch_backdrop(name):
    """
    切换背景
    :param name:
    :return:
    """
    global _current_backdrop
    global _backdrops
    global _backdrop_key
    if name not in _backdrops:
        add_backdrop(name)
    _current_backdrop = _backdrops[name]
    _backdrop_key = name


def next_backdrop():
    """
    下一个背景
    :return:
    """
    global _current_backdrop
    global _backdrop_key
    keys = list(_backdrops.keys())
    size = len(keys)
    if size == 0:
        return

    index = keys.index(_backdrop_key)
    if index >= size - 1:
        index = 0
    else:
        index = index + 1

    switch_backdrop(keys[index])


def remove_backdrop(name):
    """
    删除背景
    :param name:
    :return:
    """
    global _current_backdrop
    global _backdrops
    if name in _backdrops:
        del _backdrops[name]


class Sprite(object):
    def __init__(self, sprite_name, center_x=0, center_y=0):
        """
        定义一个角色对象
        :param sprite_name: 角色名称，该名称也对应default_sprite_image_folder定义的文件夹下面的角色图片所在的文件夹
        :param center_x:
        :param center_y:
        """
        global _sprites_max_id
        _sprites_max_id = _sprites_max_id + 1
        self.id = sprite_name + str(_sprites_max_id)
        self.sprite_name = sprite_name
        self.size = 100
        self.direction = 0
        self.timer_start = time.perf_counter()
        self.event_watcher = {}
        self.costume = {}
        self.text = None
        self.text_end_time = None
        self.showing = True
        sprite_image_name = sprite_name
        if not os.path.exists(sprite_image_name):
            sprite_image_name = default_sprite_image_folder + sprite_image_name

        for file_name in os.listdir(sprite_image_name):
            file_name_key = os.path.splitext(file_name)[0]
            self.costume[file_name_key] = os.path.join(sprite_image_name, file_name)  # open(os.path.join(name,file_name), 'r')

        current_costume = list(self.costume.items())[0]
        self.current_costume_key = current_costume[0]
        self.current_costume_value = current_costume[1]

        self.proto_sprite = pygame.image.load(self.current_costume_value).convert_alpha()
        self.sprite = self.proto_sprite

        self.rect = self.sprite.get_rect()  # rect(1,2,3,4) #  self.sprite.get_rect()
        width = self.rect.width
        height = self.rect.height
        self.rect.x = center_x - width / 2
        self.rect.y = center_y - height / 2
        self.center_x = center_x  # 存这个浮点数的原因是，pygame里面的坐标是整数，如果改变坐标的值小于1，那么里面的坐标实际上不会移动
        self.center_y = center_y  # 还有一个原因是，坐标都是角色左上角的位置，但是角度计算都是计算角色中心点，存这2个值方便计算
        self.rotate_angle = 0

        _sprites_in_game[self.id] = self
        self.event(EVENT_SPRITE_CREATED, self)

    def move(self, steps):
        """
        根据角色的direction（这是一个角度）移动，会根据direction计算出x和y分别移动的像素值
        :param steps:
        :return:
        """
        direction_pi = math.pi * (self.direction / 180)  # to π

        steps_x = steps * math.cos(direction_pi)
        steps_y = steps * math.sin(direction_pi)
        self.go_to(self.center_x + steps_x, self.center_y + steps_y)

    def turn_right(self, degrees):
        """
        向右旋转
        :param degrees:
        :return:
        """
        self.turn(-degrees)

    def turn_left(self, degrees):
        """
        向左旋转
        :param degrees:
        :return:
        """
        self.turn(degrees)

    def go_to(self, new_x, new_y):
        """
        移到新的坐标
        :param new_x:
        :param new_y:
        :return:
        """
        self.set_x_to(new_x)
        self.set_y_to(new_y)

    def go_to_random_position(self):
        """
        移到窗口内随机位置
        :return:
        """
        random_x = random.randint(0, max_x)
        random_y = random.randint(0, max_y)
        self.go_to(random_x, random_y)

    def go_to_mouse_pointer(self):
        """
        移到鼠标所在位置
        :return:
        """
        self.go_to(mouse_position[0], mouse_position[1])

    def point(self, direction):
        """
        指向特定角度，正右为0度，按照顺时针累加，正上为-90度，正下90度，正左为180度或-180度。
        :param direction:
        :return:
        """
        self.direction = direction

    def point_to(self, center_x, center_y):
        """
        指向特定坐标
        :param center_x:
        :param center_y:
        :return:
        """
        direction_pi = math.atan2(center_y - self.center_y, center_x - self.center_x)
        self.direction = (direction_pi * 180) / math.pi

    def point_to_sprite(self, target_sprite):
        """
        指定特定角色
        :param target_sprite:
        :return:
        """
        self.point_to(target_sprite.center_x, target_sprite.center_y)

    def point_towards_mouse_pointer(self):
        """
        指向鼠标所在位置
        :return:
        """
        mouse_x = mouse_position[0]
        mouse_y = mouse_position[1]
        self.point_to(mouse_x, mouse_y)

    def change_x_by(self, change_x):
        """
        调整x坐标
        :param change_x: 要调整的值
        :return:
        """
        self.center_x = self.center_x + change_x
        self._adjust_position()

    def set_x_to(self, new_x):
        """
        设置x坐标
        :param new_x: 要设置的新值
        :return:
        """
        self.center_x = new_x
        self._adjust_position()

    def change_y_by(self, change_y):
        """
        调整y坐标
        :param change_y: 要调整的值
        :return:
        """
        self.center_y = self.center_y + change_y
        self._adjust_position()

    def set_y_to(self, new_y):
        """
        设置y坐标
        :param new_y: 要设置的新值
        :return:
        """
        self.center_y = new_y
        self._adjust_position()

    def touching_edge(self):
        """
        判断是否在边缘
        :return:
        """
        if self.rect.x >= max_x - self.rect.width or self.rect.x <= 0 or self.rect.y >= max_y - self.rect.height or self.rect.y <= 0:
            return True
        return False

    def bounce_if_on_edge(self):
        """
        如果碰到边缘就反弹
        :return:
        """
        if self.rect.x >= max_x - self.rect.width:
            self.direction = 180 - self.direction
        elif self.rect.x <= 0:
            self.direction = 180 - self.direction
        elif self.rect.y >= max_y - self.rect.height:
            self.direction = - self.direction
        elif self.rect.y <= 0:
            self.direction = - self.direction

    def _adjust_position(self):
        max_center_x = max_x - self.rect.width / 2
        max_center_y = max_y - self.rect.height / 2
        if self.center_x > max_center_x:
            self.center_x = max_center_x
        if self.center_x < self.rect.width / 2:
            self.center_x = self.rect.width / 2
        if self.center_y > max_center_y:
            self.center_y = max_center_y
        if self.center_y < self.rect.height / 2:
            self.center_y = self.rect.height / 2
        self.rect.x = self.center_x - self.rect.width / 2
        self.rect.y = self.center_y - self.rect.height / 2

    def flip(self):
        """
        翻转
        :return:
        """
        self.sprite = pygame.transform.flip(self.sprite, True, False)

    def turn(self, degrees):
        self.rotate_angle += degrees
        self.direction = self.direction + degrees

    # Looks
    def say(self, text_str, size=20, color=(128, 128, 128), bg_color=None):
        """
        角色标注，可以在角色旁边显示一段文字
        :param text_str: 文字内容
        :param size: 字体大小
        :param color: 字体颜色
        :param bg_color: 字体背景颜色
        :return:
        """
        self.say_for_seconds(text_str, None, size, color, bg_color)

    def say_for_seconds(self, text_str, secs=2, size=20, color=(128, 128, 128), bg_color=None):
        """
        角色标注，可以在角色旁边显示一段文字, 若干秒后会消失
        :param text_str: 文字内容
        :param secs: 存在秒数
        :param size: 字体大小
        :param color: 字体颜色
        :param bg_color: 字体背景颜色
        :return:
        """
        font = pygame.font.Font(default_font_name, size)
        text_image = font.render(str(text_str), True, color)  # ,(128,128,128)
        self.text = {"text": text_str, "size": size, "text_image": text_image, "bg_color": bg_color}
        if secs is not None:
            self.text_end_time = time.perf_counter() + secs
        else:
            self.text_end_time = None

    def switch_costume_to(self, name):
        """
        切换造型
        :param name: 造型名称（也就是图片去掉扩展名的名称）
        :return:
        """
        if name != self.current_costume_key:
            self.current_costume_key = name
            self.current_costume_value = self.costume.get(name)
            new_sprite = pygame.image.load(self.current_costume_value).convert_alpha()
            self.proto_sprite = new_sprite
            self.set_size_to(self.size)

    def next_costume(self):
        """
        下一个造型
        :return:
        """
        keys = list(self.costume.keys())
        size = len(keys)
        index = keys.index(self.current_costume_key)
        if index >= size - 1:
            index = 0
        else:
            index = index + 1
        self.switch_costume_to(keys[index])

    def set_size_to(self, num):
        """
        修改大小
        :param num: 新的大小，100就是100%，1就是缩放为1%
        :return:
        """
        proto_rect = self.proto_sprite.get_rect()
        width = proto_rect.width
        height = proto_rect.height
        new_width = int(width * (num / 100))
        new_height = int(height * (num / 100))
        self.sprite = pygame.transform.smoothscale(self.proto_sprite, (new_width, new_height))
        self.rect.width = new_width
        self.rect.height = new_height
        self.rect.x = self.center_x - new_width / 2
        self.rect.y = self.center_y - new_height / 2
        self.size = num

    def change_size_by(self, size_by):
        """
        调整大小
        :param size_by: 调整的数量
        :return:
        """
        new_size = self.size + size_by
        if new_size > 0:
            self.set_size_to(new_size)

    def show(self):
        """
        显示
        :return:
        """
        self.showing = True

    def hide(self):
        """
        隐藏
        :return:
        """
        self.showing = False

    def action(self):
        """
        角色在每帧的活动情况，比如如果希望角色不断移动1步，就可以重载这个方法，里面加入self.move(1)的代码
        :return:
        """
        pass

    def goto_front_layer(self):
        """
        显示在前面
        :return:
        """
        global _sprites_in_game
        s = _sprites_in_game[self.id]
        del _sprites_in_game[self.id]
        _sprites_in_game[self.id] = s

    def goto_back_layer(self):
        """
        显示在后面
        :return:
        """
        global _sprites_in_game
        s = _sprites_in_game[self.id]
        del _sprites_in_game[self.id]
        new_dict = OrderedDict()
        new_dict[self.id] = s
        for k, v in list(_sprites_in_game.items()):
            new_dict[k] = v
        _sprites_in_game = new_dict

    # Events
    def regist_event(self, event_name, func):
        """
        监听事件
        :param event_name: 事件名称
        :param func: 事件发生时，调用的函数
        :return:
        """
        if event_name in self.event_watcher:
            functions = self.event_watcher.get(event_name)
            functions.append(func)
        else:
            self.event_watcher[event_name] = [func]

    def when_start(self, func):
        """
        监听游戏启动事件
        :param func:
        :return:
        """
        self.regist_event(EVENT_START, func)

    def when_key_pressed(self, key_name, func):
        """
        监听键盘按住事件
        :param key_name: 键名
        :param func:
        :return:
        """
        self.regist_event(_get_key_down_event_name(key_name), func)

    def when_key_up(self, key_name, func):
        """
        监听键盘松开事件
        :param key_name: 键名
        :param func:
        :return:
        """
        self.regist_event(_get_key_up_event_name(key_name), func)

    def when_created(self, func):
        """
        监听角色创建事件
        :param func:
        :return:
        """
        self.regist_event(EVENT_SPRITE_CREATED, func)

    def broadcast(self, event_name):
        """
        广播事件
        :param event_name:
        :return:
        """
        global_event(event_name)

    # Sensing
    def get_touching_sprite(self, sprite_name):
        """
        获取接触到的角色
        :param sprite_name: 接触的角色名称
        :return:
        """
        sprites = []
        self_pygame_rect = self.rect
        for sprite in list(_sprites_in_game.values()):
            if sprite.sprite_name == sprite_name:
                if pygame.Rect.colliderect(self_pygame_rect, sprite.rect):
                    sprites.append(sprite)
        return sprites

    def get_closest_sprite_by_name(self, sprite_name):
        """
        获取最近的特定角色
        :param sprite_name: 角色名称
        :return:
        """
        sprites = get_sprites_by_name(sprite_name)
        return self.get_closest_sprite(sprites)

    def get_closest_sprite(self, sprites):
        """
        从角色列表中找出离自己最近的
        :param sprites: 角色列表
        :return:
        """
        min_distance = 9999
        closest_sprite = None
        self_point = (self.center_x, self.center_y)
        for sprite in sprites:
            distance = get_distance(self_point, (sprite.center_x, sprite.center_y))
            if min_distance > distance:
                min_distance = distance
                closest_sprite = sprite
        return closest_sprite

    def reset_timer(self):
        """
        重置定时器
        :return:
        """
        self.timer_start = time.perf_counter()

    def timer(self):
        """
        上次定时后到目前的秒数
        :return:
        """
        return time.perf_counter() - self.timer_start

    def event(self, event_name, *args, **kwargs):
        """
        触发事件
        :param event_name:
        :param args:
        :param kwargs:
        :return:
        """
        if event_name in self.event_watcher:
            functions = self.event_watcher.get(event_name)
            for func in functions:
                func(*args, **kwargs)

    def delete(self):
        """
        删除自己
        :return:
        """
        self.hide()
        if self.id in _sprites_in_game.keys():
            del _sprites_in_game[self.id]

# encoding: utf-8
# module pygamescratch
#
import math
import os
import sys
import threading
import time
import traceback
from collections import OrderedDict

import pygame
from pygame.locals import *

# 以下是默认事件名称，可以引用
EVENT_MOUSE_LEFT = "_EVENT_MOUSE_LEFT"
EVENT_MOUSE_RIGHT = "_EVENT_MOUSE_RIGHT"
EVENT_MOUSE_MIDDLE = "_EVENT_MOUSE_MIDDLE"
EVENT_START = "EVENT_START"
EVENT_SPRITE_CREATED = "_EVENT_SPRITE_CREATED"

# 以下是私有变量，不对外
_EVENT_KEY_UP = "_EVENT_KEY_UP"
_EVENT_KEY_DOWN = "_EVENT_KEY_DOWN"

pygame.init()
pygame.font.init()


class PygameScratch:

    def __init__(self) -> None:
        self._game_running = True  # 当前游戏是否在运行
        self._fps = 60  # 帧数
        self._time_piece = 1 / self._fps  # 每帧时间间隔

        self._screen = None  # pygame的screen对象
        self._events = OrderedDict()  # 存放所有触发的事件
        self._global_event_watcher = {}  # 存放所有的事件监听器
        self._delay_functions = []  # 存放所有待延迟执行的函数
        self._current_backdrop = None  # 当前背景
        self._backdrop_key = None  # 当前背景key
        self._backdrops = OrderedDict()  # 存放所有背景的map
        self.sprites_in_game = OrderedDict()  # 存放所有角色对象
        self._sprites_max_id = 0  # 每创建一个角色就会赋予一个编号，该变量存放当前最大的角色编号

        self._texts = OrderedDict()  # 存放要显示在screen中的所有文本，文本id为主键
        self._key_down_list = []  # 存放当前按住的键位列表
        self._default_screen_size = (470, 700)  # 默认窗口大小

        # 以下是默认参数，外部可以修改
        self.default_music_folder = "./music/"  # 默认音乐文件夹
        self.default_font_folder = "./font/"  # 默认字体文件夹
        self.default_sprite_image_folder = "./images/sprite/"  # 默认角色文件夹
        self.default_backdrop_image_folder = "./images/backdrop/"  # 默认字体文件夹
        self.default_backdrop_color = (255, 255, 255)  # 默认背景色
        self.default_font_name = pygame.font.match_font("幼圆")  # 默认字体名称
        self.default_key_repeat_delay = 20  # 按压键盘重复触发key down事件的间隔
        self.max_x, self.max_y = self._default_screen_size
        self.screen_center_x, self.screen_center_y = (self.max_x / 2, self.max_y / 2)
        # 以下是公共变量，可以访问
        self.mouse_position = (0, 0)  # 存放当前鼠标的位置
        self.game_paused = False  # 当前游戏是否暂停

    def screen_size(self, width, height):
        """
        修改屏幕大小
        :param width:
        :param height:
        :return:
        """
        self._default_screen_size = (width, height)
        self.max_x, self.max_y = self._default_screen_size
        self.screen_center_x, self.screen_center_y = (self.max_x / 2, self.max_y / 2)

    def text(self, text_id, text_str, x, y, size=40, color=(128, 128, 128)):
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
        text_font = pygame.font.Font(self.default_font_name, size)
        text_image = text_font.render(text_str, True, color)
        new_text = {"text": text_str, "x": x, "y": y, "size": size, "image": text_image}
        self._texts[text_id] = new_text
        return new_text

    def remove_text(self, text_id):
        """
        移除文字
        :param text_id: 要移除的文字id
        :return:
        """
        if text_id:
            if text_id in self._texts.keys():
                del self._texts[text_id]

    def clear_text(self):
        """
        移除所有文字
        :return:
        """
        self._texts.clear()

    def get_sprites_by_name(self, sprite_name):
        """
        根据角色名称返回角色列表
        :param sprite_name: 角色名称
        :return: 对应名称的所有角色列表
        """
        sprites = []
        for s in list(self.sprites_in_game.values()):
            if s.sprite_name == sprite_name:
                sprites.append(s)
        return sprites

    def refresh_events(self):
        """
        刷新事件列表，前一帧之前触发的事件都会被清除，不管有没有触发过
        """
        new_events = {}
        start_time = time.perf_counter()
        for event_name, time_list in self._events.items():
            new_time_list = []
            for event_time in time_list:
                if event_time > start_time - self._time_piece:  # not too old
                    new_time_list.append(event_time)
            if len(new_time_list) > 0:
                new_events[event_name] = new_time_list
        self._events = new_events

    def schedule(self, delay_seconds, func, repeat_interval, *args, **kwargs):
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
        self._delay_functions.append(func_data)

    def _execute_delay_functions(self):
        current_time = time.perf_counter()
        for func_data in list(self._delay_functions):
            if func_data[0] <= current_time:
                func_data[1](*func_data[3], **func_data[4])
                if func_data[2] is not None and func_data[2] > 0:
                    func_data[0] = current_time + func_data[2]
                elif func_data in self._delay_functions:
                    self._delay_functions.remove(func_data)

    def delete_delay_function_by_object(self, obj):
        """
        删除该角色下的所有定时任务
        :param obj: 角色对象
        :return:
        """
        for delay_function in list(self._delay_functions):
            if "__self__" in dir(delay_function[1]):
                if obj == delay_function[1].__self__:
                    if delay_function in self._delay_functions:
                        self._delay_functions.remove(delay_function)

    def play_sound(self, sound):
        """
        播放音乐
        :param sound: 音乐文件的名称（包含扩展名），函数会自动在default_music_folder定义的文件夹下面寻找对应的音乐文件
        :return:
        """
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        sound_file = pygame.mixer.Sound(self.default_music_folder + sound)
        sound_file.play()

    def background_music_load(self, music_name):
        """
        载入背景音乐
        :param music_name: 音乐文件的名称（包含扩展名），函数会自动在default_music_folder定义的文件夹下面寻找对应的音乐文件
        :return:
        """
        try:
            pygame.mixer.music.load(self.default_music_folder + music_name)  # 游戏背景音乐
            pygame.mixer.music.set_volume(0.6)  # 设置音量(0-1)
            pygame.mixer.music.play(-1)  # 循环播放
        except Exception as e:
            raise

    def _sprites_frame_action(self):
        for s in list(self.sprites_in_game.values()):
            if not s.image.get_locked():
                s.action()

    def _update_screen(self):
        if not self._game_running:
            return
        # draw back ground
        if self._current_backdrop:
            self._display_backdrop(self._screen, self._current_backdrop)
        else:
            self._screen.fill(self.default_backdrop_color)
        # draw all sprite
        for s in list(self.sprites_in_game.values()):
            if not s.image.get_locked() and s.showing:
                rect = s.rect
                if s.rotate_angle != 0:
                    new_sprite = pygame.transform.rotate(s.image, s.rotate_angle)
                    self._screen.blit(new_sprite, rect)
                else:
                    self._screen.blit(s.image, rect)
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
                        pygame.draw.circle(self._screen, s.text['bg_color'], [text_x, text_y], text_rect.width / 2 + 2,
                                           text_rect.width + 2)
                    self._screen.blit(text_image, (text_x, text_y))

        for t in self._texts.values():
            start_x = t['x']
            start_y = t['y']
            self._screen.blit(t['image'], (start_x, start_y))

        pygame.display.update()

    def _display_backdrop(self, screen, backdrop):
        image_ = backdrop["image"]
        if image_.get_locked():
            return
        screen.blit(image_, (backdrop["x"], backdrop["y"]))
        rect = image_.get_rect()
        if backdrop["x"] < 0 and backdrop["x"] + rect.width < self.max_x:
            screen.blit(image_, (backdrop["x"] + rect.width, backdrop["y"]))
        if backdrop["x"] > 0:
            screen.blit(image_, (backdrop["x"] - rect.width, backdrop["y"]))
        if backdrop["y"] < 0 and backdrop["y"] + rect.height < self.max_y:
            screen.blit(image_, (backdrop["x"], backdrop["y"] + rect.height))
        if backdrop["y"] > 0:
            screen.blit(image_, (backdrop["x"], backdrop["y"] - rect.height))
        if not self.game_paused:
            backdrop["x"] = backdrop["x"] + backdrop["moving_x"]
            backdrop["y"] = backdrop["y"] + backdrop["moving_y"]
            if backdrop["x"] < -rect.width or backdrop["x"] > rect.width:
                backdrop["x"] = 0
            if backdrop["y"] < -rect.height or backdrop["y"] > rect.height:
                backdrop["y"] = 0

    def _frame_loop(self):
        while self._game_running:
            try:

                # time fragment
                start_time = time.perf_counter()
                if not self.game_paused:
                    # event
                    self.refresh_events()
                    # events.clear()
                    self._execute_delay_functions()
                    self._sprites_frame_action()
                self._update_screen()
                elapsed = time.perf_counter() - start_time

                if self._time_piece > elapsed:
                    time.sleep(self._time_piece - elapsed)
            except Exception as e:
                self.print_exception(e)

    def print_exception(self, e):
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

    def global_event(self, event_name, *args, **kwargs):
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
        if event_name in self._events:
            self._events[event_name].append(event_time)
        else:
            self._events[event_name] = [event_time]

        self._trigger_global_event(event_name, *args, **kwargs)
        if not self.game_paused:
            for s in list(self.sprites_in_game.values()):
                s.event(event_name, *args, **kwargs)

    def regist_global_event(self, event_name, func):
        """
        全局范围内注册事件监听器
        :param event_name: 监听的事件名称
        :param func: 待触发的函数
        :return:
        """
        if event_name in self._global_event_watcher:
            functions = self._global_event_watcher.get(event_name)
            functions.append(func)
        else:
            self._global_event_watcher[event_name] = [func]

    def when_key_pressed(self, key_name, func):
        """
        注册按键事件监听器
        :param key_name: 监听的按键值
        :param func: 待触发的函数
        :return:
        """
        self.regist_global_event(self._get_key_down_event_name(key_name), func)

    def when_key_up(self, key_name, func):
        """
        注册松开按键事件
        :param key_name: 监听的松开的按键值
        :param func: 待触发的函数
        :return:
        """
        self.regist_global_event(self._get_key_up_event_name(key_name), func)

    def _trigger_global_event(self, event_name, *args, **kwargs):
        if event_name in self._global_event_watcher:
            functions = self._global_event_watcher.get(event_name)
            for func in functions:
                func(*args, **kwargs)

    def game_name(self, name):
        """
        设置游戏名称
        :param name: 游戏名称
        :return:
        """
        pygame.display.set_caption(name)

    def is_key_pressed(self, key):
        """
        判断该键是否按住
        :param key: 要判断的按键值
        :return:
        """
        return key in self._key_down_list

    def get_distance(self, point1, point2):
        """
        获取两个坐标之间的距离
        :param point1:
        :param point2:
        :return:
        """
        return math.sqrt(pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))

    def _get_events(self):
        pos = pygame.mouse.get_pos()
        self.mouse_position = (pos[0]), (pos[1])

        for event in pygame.event.get():
            if event.type == QUIT:
                self._game_running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not (event.key in self._key_down_list):
                    self._key_down_list.append(event.key)
                self.global_event(self._get_key_down_event_name(event.key))
            if event.type == pygame.KEYUP:
                self._key_down_list.remove(event.key)
                self.global_event(self._get_key_up_event_name(event.key))
            if event.type == MOUSEBUTTONDOWN:  # 鼠标按下
                pressed_array = pygame.mouse.get_pressed()  # 获得鼠标点击类型[0,1,2] 左键,滑轮,右键
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:  # 点击了鼠标左键
                            self.global_event(EVENT_MOUSE_LEFT)
                        if index == 1:  # 点击了鼠标中键
                            self.global_event(EVENT_MOUSE_MIDDLE)
                        if index == 2:  # 点击了鼠标右键
                            self.global_event(EVENT_MOUSE_RIGHT)

    @staticmethod
    def _get_key_up_event_name(key):
        return _EVENT_KEY_UP + str(key)

    @staticmethod
    def _get_key_down_event_name(key):
        return _EVENT_KEY_DOWN + str(key)

    def start(self):
        """
        开始游戏，该方法会初始化pygame，并且做两件事情，
        一是在主线程循环获取键盘和鼠标事件，并触发相应事件监听器
        二是启动一个线程，该线程会每帧重复执行：清除过期事件、执行角色活动、执行定时任务、渲染窗口，
        :return:
        """
        self._screen = pygame.display.set_mode(self._default_screen_size)

        self._screen.fill(self.default_backdrop_color)
        pygame.key.set_repeat(self.default_key_repeat_delay)

        self._game_running = True
        self.global_event(EVENT_START)
        threading.Thread(target=self._frame_loop).start()

        while self._game_running:
            try:
                self._get_events()
                time.sleep(0.01)
            except Exception as e:
                self.print_exception(e)

    def add_backdrop(self, name, moving_x=0, moving_y=0):
        """
        增加背景
        :param name: 背景文件路径，可以传入完整路径，也可以只传入背景文件名，程序会自动到default_backdrop_image_folder定义的文件夹中找到以jpg结尾的同名的图片
        :param moving_x: 背景每帧x的变化值，可用来做移动背景
        :param moving_y: 背景每帧y的变化值
        :return:
        """
        if os.path.exists(name):
            backdrop_image = pygame.image.load(name).convert_alpha()
        else:
            if not name.endswith(".jpg"):
                path = self.default_backdrop_image_folder + name + ".jpg"
            backdrop_image = pygame.image.load(path).convert_alpha()
        backdrop = {"x": 0, "y": 0, "image": backdrop_image, "moving_x": moving_x, "moving_y": moving_y}
        self._backdrops[name] = backdrop
        self._current_backdrop = backdrop
        self._backdrop_key = name

    def switch_backdrop(self, name):
        """
        切换背景
        :param name:
        :return:
        """
        if name not in self._backdrops:
            self.add_backdrop(name)
        self._current_backdrop = self._backdrops[name]
        self._backdrop_key = name

    def next_backdrop(self):
        """
        下一个背景
        :return:
        """
        keys = list(self._backdrops.keys())
        size = len(keys)
        if size == 0:
            return

        index = keys.index(self._backdrop_key)
        if index >= size - 1:
            index = 0
        else:
            index = index + 1

        self.switch_backdrop(keys[index])

    def remove_backdrop(self, name):
        """
        删除背景
        :param name:
        :return:
        """
        if name in self._backdrops:
            del self._backdrops[name]

    def clear_backdrop(self):
        """
        删除所有背景
        :return:
        """
        self._backdrops.clear()

    def clear_sprites(self):
        """
        删除所有角色，请注意，角色的延时函数并不会被删除
        :return:
        """
        self.sprites_in_game.clear()

    def clear_schedule(self):
        """
        删除所有定时器
        :return:
        """
        self._delay_functions.clear()


pygs = PygameScratch()

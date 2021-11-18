import random

from .pygs import *


class Sprite(object):
    def __init__(self, sprite_name, center_x=0, center_y=0):
        """
        定义一个角色对象
        :param sprite_name: 角色名称，该名称也对应default_sprite_image_folder定义的文件夹下面的角色图片所在的文件夹
        :param center_x:
        :param center_y:
        """
        pygs._sprites_max_id = pygs._sprites_max_id + 1
        self.id = sprite_name + str(pygs._sprites_max_id)
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
            sprite_image_name = pygs.default_sprite_image_folder + sprite_image_name

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

        pygs.sprites_in_game[self.id] = self
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
        random_x = random.randint(0, pygs.max_x)
        random_y = random.randint(0, pygs.max_y)
        self.go_to(random_x, random_y)

    def go_to_mouse_pointer(self):
        """
        移到鼠标所在位置
        :return:
        """
        self.go_to(pygs.mouse_position[0], pygs.mouse_position[1])

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
        mouse_x = pygs.mouse_position[0]
        mouse_y = pygs.mouse_position[1]
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
        if self.rect.x >= pygs.max_x - self.rect.width or self.rect.x <= 0 or self.rect.y >= pygs.max_y - self.rect.height or self.rect.y <= 0:
            return True
        return False

    def bounce_if_on_edge(self):
        """
        如果碰到边缘就反弹
        :return:
        """
        if self.rect.x >= pygs.max_x - self.rect.width:
            self.direction = 180 - self.direction
        elif self.rect.x <= 0:
            self.direction = 180 - self.direction
        elif self.rect.y >= pygs.max_y - self.rect.height:
            self.direction = - self.direction
        elif self.rect.y <= 0:
            self.direction = - self.direction

    def _adjust_position(self):
        max_center_x = pygs.max_x - self.rect.width / 2
        max_center_y = pygs.max_y - self.rect.height / 2
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
        font = pygame.font.Font(pygs.default_font_name, size)
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
        s = pygs.sprites_in_game[self.id]
        del pygs.sprites_in_game[self.id]
        pygs.sprites_in_game[self.id] = s

    def goto_back_layer(self):
        """
        显示在后面
        :return:
        """
        s = pygs.sprites_in_game[self.id]
        del pygs.sprites_in_game[self.id]
        new_dict = OrderedDict()
        new_dict[self.id] = s
        for k, v in list(pygs.sprites_in_game.items()):
            new_dict[k] = v
        sprites_in_game = new_dict

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
        self.regist_event(pygs._get_key_down_event_name(key_name), func)

    def when_key_up(self, key_name, func):
        """
        监听键盘松开事件
        :param key_name: 键名
        :param func:
        :return:
        """
        self.regist_event(pygs._get_key_up_event_name(key_name), func)

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
        pygs.global_event(event_name)

    # Sensing
    def get_touching_sprite(self, sprite_name):
        """
        获取接触到的角色
        :param sprite_name: 接触的角色名称
        :return:
        """
        sprites = []
        self_pygame_rect = self.rect
        for sprite in list(pygs.sprites_in_game.values()):
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
        sprites = pygs.get_sprites_by_name(sprite_name)
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
            distance = pygs.get_distance(self_point, (sprite.center_x, sprite.center_y))
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
        if self.id in pygs.sprites_in_game.keys():
            del pygs.sprites_in_game[self.id]
            pygs.delete_delay_function_by_object(self)

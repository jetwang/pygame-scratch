### pygamescratch是什么？
pygamescratch是个python库，让学习scratch的小孩更容易上手python编写游戏。


### 如何使用pygamescratch?
```bash
pip install pygamescratch
```

###  示例代码
src/sample-planefight 里面有较复杂的示例，玩一个飞机大战的小游戏

src/sample-simple 里面是简单示例，一只猫向一只球移动，碰到球球就消失

### 如何运行飞机大战示例
```bash
cd src/sample-planefight
pip install pygamescratch
python plane_fight.py
```
### 飞机大战示例使用说明
1. 移动： WASD四个按键
2. 射击： 鼠标左键射一个子弹，鼠标右键射三个子弹，可长按鼠标。可连射的子弹数有控制，可通过吃物品增加。
3. 召唤盟友：鼠标中键，减掉3个血

### pygamescratch 接口使用手册：


Sprite类
    
    class Sprite(builtins.object)
     |  Sprite(sprite_name, x=0, y=0)
     |  
     |  Methods defined here:
     |  
     |  __init__(self, sprite_name, x=0, y=0)
     |      定义一个角色对象
     |      :param sprite_name: 角色名称，该名称也对应default_sprite_image_folder定义的文件夹下面的角色图片所在的文件夹
     |      :param x:
     |      :param y:
     |  
     |  action(self)
     |      角色在每帧的活动情况，比如如果希望角色不断移动1步，就可以重载这个方法，里面加入self.move(1)的代码
     |      :return:
     |  
     |  bounce_if_on_edge(self)
     |      如果碰到边缘就反弹
     |      :return:
     |  
     |  broadcast(self, event_name)
     |      广播事件
     |      :param event_name:
     |      :return:
     |  
     |  change_size_by(self, size_by)
     |      调整大小
     |      :param size_by: 调整的数量
     |      :return:
     |  
     |  change_x_by(self, change_x)
     |      调整x坐标
     |      :param change_x: 要调整的值
     |      :return:
     |  
     |  change_y_by(self, change_y)
     |      调整y坐标
     |      :param change_y: 要调整的值
     |      :return:
     |  
     |  delete(self)
     |      删除自己
     |      :return:
     |  
     |  event(self, event_name, *args, **kwargs)
     |      触发事件
     |      :param event_name:
     |      :param args:
     |      :param kwargs:
     |      :return:
     |  
     |  flip(self)
     |      翻转
     |      :return:
     |  
     |  get_closest_sprite(self, sprites)
     |      从角色列表中找出离自己最近的
     |      :param sprites: 角色列表
     |      :return:
     |  
     |  get_closest_sprite_by_name(self, sprite_name)
     |      获取最近的特定角色
     |      :param sprite_name: 角色名称
     |      :return:
     |  
     |  get_touching_sprite(self, sprite_name)
     |      获取接触到的角色
     |      :param sprite_name: 接触的角色名称
     |      :return:
     |  
     |  go_to(self, new_x, new_y)
     |      移到新的坐标
     |      :param new_x:
     |      :param new_y:
     |      :return:
     |  
     |  go_to_mouse_pointer(self)
     |      移到鼠标所在位置
     |      :return:
     |  
     |  go_to_random_position(self)
     |      移到窗口内随机位置
     |      :return:
     |  
     |  goto_back_layer(self)
     |      显示在后面
     |      :return:
     |  
     |  goto_front_layer(self)
     |      显示在前面
     |      :return:
     |  
     |  hide(self)
     |      隐藏
     |      :return:
     |  
     |  move(self, steps)
     |      根据角色的direction（这是一个角度）移动，会根据direction计算出x和y分别移动的像素值
     |      :param steps:
     |      :return:
     |  
     |  next_costume(self)
     |      下一个造型
     |      :return:
     |  
     |  point(self, direction)
     |      指向特定角度，正上方为0度，正右为90度，正下180度，正左为270度。
     |      :param direction:
     |      :return:
     |  
     |  point_to(self, x, y)
     |      指向特定坐标
     |      :param x:
     |      :param y:
     |      :return:
     |  
     |  point_towards_mouse_pointer(self)
     |      指向鼠标所在位置
     |      :return:
     |  
     |  regist_event(self, event_name, func)
     |      监听事件
     |      :param event_name: 事件名称
     |      :param func: 事件发生时，调用的函数
     |      :return:
     |  
     |  reset_timer(self)
     |      重置定时器
     |      :return:
     |  
     |  say(self, text_str, size=20, color=(128, 128, 128), bg_color=None)
     |      角色标注，可以在角色旁边显示一段文字
     |      :param text_str: 文字内容
     |      :param size: 字体大小
     |      :param color: 字体颜色
     |      :param bg_color: 字体背景颜色
     |      :return:
     |  
     |  say_for_seconds(self, text_str, secs=2, size=20, color=(128, 128, 128), bg_color=None)
     |      角色标注，可以在角色旁边显示一段文字, 若干秒后会消失
     |      :param text_str: 文字内容
     |      :param secs: 存在秒数
     |      :param size: 字体大小
     |      :param color: 字体颜色
     |      :param bg_color: 字体背景颜色
     |      :return:
     |  
     |  set_size_to(self, num)
     |      修改大小
     |      :param num: 新的大小，100就是100%，1就是缩放为1%
     |      :return:
     |  
     |  set_x_to(self, new_x)
     |      设置x坐标
     |      :param new_x: 要设置的新值
     |      :return:
     |  
     |  set_y_to(self, new_y)
     |      设置y坐标
     |      :param new_y: 要设置的新值
     |      :return:
     |  
     |  show(self)
     |      显示
     |      :return:
     |  
     |  switch_costume_to(self, name)
     |      切换造型
     |      :param name: 造型名称（也就是图片去掉扩展名的名称）
     |      :return:
     |  
     |  timer(self)
     |      上次定时后到目前的秒数
     |      :return:
     |  
     |  touching_edge(self)
     |      判断是否在边缘
     |      :return:
     |  
     |  turn(self, degrees)
     |  
     |  turn_left(self, degrees)
     |      向左旋转
     |      :param degrees:
     |      :return:
     |  
     |  turn_right(self, degrees)
     |      向右旋转
     |      :param degrees:
     |      :return:
     |  
     |  when_created(self, func)
     |      监听角色创建事件
     |      :param func:
     |      :return:
     |  
     |  when_key_pressed(self, key_name, func)
     |      监听键盘按住事件
     |      :param key_name: 键名
     |      :param func:
     |      :return:
     |  
     |  when_key_up(self, key_name, func)
     |      监听键盘松开事件
     |      :param key_name: 键名
     |      :param func:
     |      :return:
     |  
     |  when_start(self, func)
     |      监听游戏启动事件
     |      :param func:
     |      :return:
     |  
     |  ----------------------------------------------------------------------

全局函数

    add_backdrop(name)
        增加背景
        :param name: 背景文件路径，可以传入完整路径，也可以只传入背景文件名，程序会自动到default_backdrop_image_folder定义的文件夹中找到以jpg结尾的同名的图片
        :return:
    
    background_music_load(music_name)
        载入背景音乐
        :param music_name: 音乐文件的名称（包含扩展名），函数会自动在default_music_folder定义的文件夹下面寻找对应的音乐文件
        :return:
    
    clear_text()
        移除所有文字
        :return:
    
    game_name(name)
        设置游戏名称
        :param name: 游戏名称
        :return:
    
    get_distance(point1, point2)
        获取两个坐标之间的距离
        :param point1:
        :param point2:
        :return:
    
    get_sprites_by_name(sprite_name)
        根据角色名称返回角色列表
        :param sprite_name: 角色名称
        :return: 对应名称的所有角色列表
    
    global_event(event_name, *args, **kwargs)
        全局范围内触发事件
        :param event_name: 触发事件名称
        :param args: 要传入事件触发函数的可变参数
        :param kwargs: 要传入事件触发函数的关键字参数
        :return:
    
    is_key_pressed(key)
        判断该键是否按住
        :param key: 要判断的按键值
        :return:
    
    next_backdrop()
        下一个背景
        :return:
    
    play_sound(sound)
        播放音乐
        :param sound: 音乐文件的名称（包含扩展名），函数会自动在default_music_folder定义的文件夹下面寻找对应的音乐文件
        :return:
    
    print_exception(e)
        打印出异常信息
        :param e: 异常
        :return:
    
    pygame_rect(target_rect)
        获取pygame的rect对象，pygame最左上方的坐标是（0,0），而在本游戏中，中心点的坐标为（0,0），分为4个象限
        :param target_rect:
        :return:
    
    refresh_events()
        刷新事件列表，前一帧之前触发的事件都会被清除，不管有没有触发过
    
    regist_global_event(event_name, func)
        全局范围内注册事件监听器
        :param event_name: 监听的事件名称
        :param func: 待触发的函数
        :return:
    
    remove_backdrop(name)
        删除背景
        :param name:
        :return:
    
    remove_text(text_id)
        移除文字
        :param text_id: 要移除的文字id
        :return:
    
    schedule(delay_seconds, func, repeat_interval, *args, **kwargs)
        延迟执行函数
        :param delay_seconds: 等待时长
        :param func:  执行的函数对象
        :param repeat_interval: 重复执行间隔，如果为None或者不大于0，只执行一次
        :param args:  传入的无名参数
        :param kwargs:  关键字参数
        :return:
    
    start()
        开始游戏，该方法会初始化pygame，并且做两件事情，
        一是在主线程循环获取键盘和鼠标事件，并触发相应事件监听器
        二是启动一个线程，该线程会每帧重复执行：清除过期事件、执行角色活动、执行定时任务、渲染窗口，
        :return:
    
    switch_backdrop(name)
        切换背景
        :param name:
        :return:
    
    text(text_id, text_str, x=-120, y=-120, size=40, color=(128, 128, 128))
        添加一行文字，改文字会保存到一个列表当中，每次渲染的时候都会显示
        :param text_id: 文本id
        :param text_str: 要显示的字符串
        :param x: 第一个文字的x坐标
        :param y: 第一个文字的y坐标
        :param size: 字体大小
        :param color: 字体颜色
        :return: 返回该文本对象，输入的参数都成为该对象的属性
    
    when_key_pressed(key_name, func)
        注册按键事件监听器
        :param key_name: 监听的按键值
        :param func: 待触发的函数
        :return:
    
    when_key_up(key_name, func)
        注册松开按键事件
        :param key_name: 监听的松开的按键值
        :param func: 待触发的函数
        :return:
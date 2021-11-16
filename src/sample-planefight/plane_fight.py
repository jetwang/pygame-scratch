from enemy_plane import *
from hero_plane import *

pause_icon = None


def change_game_paused_state():
    global pause_icon
    pygs.game_paused = not pygs.game_paused
    if pygs.game_paused:
        if pause_icon is None:
            pause_icon = Sprite("pause", pygs.screen_center_x, pygs.screen_center_y)
        pause_icon.goto_front_layer()
        pause_icon.show()
        instructions = ["游戏暂停中，使用空格键启动游戏。",
                        "游戏说明：",
                        "1. 使用WASD四个按键移动主角；",
                        "2. 鼠标左键射一个子弹，右键射三个子弹，可长按发射；",
                        "3. 可连射的子弹数有控制，可通过吃物品增加；",
                        "4. 5颗血以上可按鼠标中键召唤盟友，会减掉3个血。"]
        y = pygs.screen_center_y
        for instruction in instructions:
            y = y + 30
            text("instruction" + str(y), instruction, x=5, y=y, size=16, color=(0, 0, 0))
    else:
        if pause_icon:
            pause_icon.hide()
            clear_text()


def create_sprites():
    add_backdrop("images/backdrop/background.png", moving_y=1)
    pygame.display.set_caption("飞机大战")
    background_music_load("PlaneWarsBackgroundMusic.mp3")
    when_key_up(g.PAUSE_KEY, change_game_paused_state)
    g.hero = HeroPlane(pygs.screen_center_x, pygs.screen_center_y - 30)
    refresh_enemy_icons()
    create_enemy()
    change_game_paused_state()


if __name__ == "__main__":
    pygs.default_font_name = g.font_name
    pygs.default_key_repeat_delay = 2000
    pygs.screen_size(470, 700)
    regist_global_event(EVENT_START, create_sprites)
    start()

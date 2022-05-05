from enemy_plane import *
from hero_plane import *
from obstacle import *
from pygamescratch import *


def change_game_paused_state():
    pygs.game_paused = not pygs.game_paused
    if pygs.game_paused:
        if g.pause_icon is None:
            g.pause_icon = Sprite("pause", pygs.screen_center_x, pygs.screen_center_y)
        g.pause_icon.goto_front_layer()
        g.pause_icon.show()
        instructions = ["游戏暂停中，使用空格键启动游戏，使用回车键重启游戏。",
                        "游戏说明：",
                        "1. 使用WASD四个按键移动主角；",
                        "2. 鼠标左键射一个子弹，右键射三个子弹，可长按发射；",
                        "3. 可连射的子弹数有控制，可通过吃物品增加；",
                        "4. 5颗血以上可按鼠标中键召唤盟友，会减掉3个血。"]
        y = pygs.screen_center_y
        for instruction in instructions:
            y = y + 30
            pygs.text("instruction" + str(y), instruction, x=5, y=y, size=16, color=(0, 0, 0))
    else:
        if g.pause_icon:
            g.pause_icon.hide()
            pygs.clear_text()


def create_enemy():
    if len(g.get_enemies()) >= g.max_enemies or len(g.pending_enemy_types) <= 0:
        pygs.schedule(g.enemy_new_wait, create_enemy, None)
        return
    x = random.randrange(0, pygs.max_x)
    y = 30
    enemy_type = g.pending_enemy_types.pop(0)
    EnemyPlane(enemy_type, x, y)
    refresh_enemy_icons()
    pygs.schedule(g.enemy_new_wait, create_enemy, None)


def refresh_enemy_icons():
    if len(g.pending_enemy_types) < 10:
        g.pending_enemy_types = g.pending_enemy_types + [0, 0, 0, 0, 1, 0, 0, 0, 1, 2]
    x = 10
    y = 10
    enemy_icon_sprites = pygs.get_sprites_by_name("enemyicon")
    if len(enemy_icon_sprites) <= 0:
        for index in range(0, 10):
            Sprite("enemyicon", x, y)
            x = x + 30
        enemy_icon_sprites = pygs.get_sprites_by_name("enemyicon")
    for index in range(0, 10):
        enemy_icon_sprites[index].switch_costume_to(str(g.pending_enemy_types[index]))


def initialize_game():
    pygs.clear_schedule()
    pygs.clear_backdrop()
    pygs.clear_sprites()
    g.__init__()
    pygs.add_backdrop("images/backdrop/background.png", moving_y=1)
    g.hero = HeroPlane(pygs.screen_center_x, pygs.screen_center_y - 30)
    g.obstacle = Obstacle(pygs.screen_center_x, pygs.screen_center_y )
    refresh_enemy_icons()
    pygs.schedule(g.enemy_new_wait, create_enemy, None)
    g.display_hero_hp()
    g.display_hero_bullet_score()
    change_game_paused_state()


if __name__ == "__main__":
    pygs.default_font_name = g.font_name
    pygs.default_key_repeat_delay = 2000
    pygs.screen_size(470, 700)
    pygame.display.set_caption("飞机大战")
    pygs.background_music_load("PlaneWarsBackgroundMusic.mp3")
    pygs.when_key_up(RESTART_KEY, initialize_game)
    pygs.regist_global_event(EVENT_START, initialize_game)
    pygs.when_key_up(PAUSE_KEY, change_game_paused_state)
    pygs.start()

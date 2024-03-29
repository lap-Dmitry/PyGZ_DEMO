import pgzrun
from game_setting import *

TILE_SIZE = 18
ROWS = 30
COLS = 20

WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "PygZ"
FPS = 30

buttons_start_game = Actor("new_game", bottomleft=(150, 100))
buttons_music_game = Actor("music_game_on", bottomleft=(150, 200))
buttons_sound_game = Actor("music_game_off", bottomleft=(150, 200))
buttons_quit_game = Actor("game_exit", bottomleft=(150, 300))

buttons_start_game.y
buttons_music_game.y
buttons_quit_game.y

buttons_start_game.start_game = False
buttons_music_game.stop_sound = True


def on_mouse_down(button, pos):
    if button == button.LEFT:
        if buttons_start_game.collidepoint(pos):
            while buttons_start_game.start_game == False:
                buttons_start_game.start_game = True
        elif buttons_music_game.collidepoint(pos):
            count = 3
            while count >= 0:
                if buttons_music_game.stop_sound == True:
                    music.stop()
                    buttons_music_game.stop_sound = False
                    break
                else:
                    buttons_music_game.stop_sound = True
                    music.play("sky")
                    break
        elif buttons_quit_game.collidepoint(pos):
            clock.schedule_unique(quit, 0.1)


def on_mouse_move(pos):
    if buttons_start_game.collidepoint(pos):
        if buttons_start_game.start_game == False:
            mouse_cursor_button_on()

    elif buttons_music_game.collidepoint(pos):
        mouse_cursor_button_on()

    elif buttons_quit_game.collidepoint(pos):
        mouse_cursor_button_on()

    elif not buttons_start_game.collidepoint(pos):
        mouse_cursor_button_off()

        def draw():
            buttons_start_game_hover.draw()

    elif not buttons_music_game.collidepoint(pos):
        mouse_cursor_button_off()

    elif not buttons_quit_game.collidepoint(pos):
        mouse_cursor_button_off()


color_key = (0, 0, 0)

tree_stand = Sprite("tree.png", (0, 0, 32, 32), 4, color_key, 30)
tree_walk = Sprite("tree.png", (0, 32, 32, 32), 8, color_key, 5)
tree_dead = Sprite("tree.png", (0, 32, 32, 32), 5, color_key, 5)

bat_walk = Sprite("bat.png", (0, 0, 16, 16), 5, color_key, 5)
bat_walk1 = Sprite("bat.png", (0, 24, 16, 16), 5, color_key, 5)

player = SpriteActor(tree_stand, bottomleft=(-100, 400))
enemys1 = SpriteActor(bat_walk, bottomleft=(500, 260))
enemys2 = SpriteActor(bat_walk1, bottomleft=(430, 140))


player.alive = True
player.jumping = False
player.velocity_x = 3
player.velocity_y = 1

jump_velocity = -10
gravity = 1
over = False
win = False
timer = 0

enemys1.x = 500
enemys2.x = 100
enemys1_x_speed = 1
enemys2_x_speed = 1


def start():
    clock.schedule_interval(increment_timer, 1.0)
    music.play("sky")


def increment_timer():
    global timer
    timer += 1


def game_win():
    global win
    win = True
    player.alive = False
    clock.schedule_unique(quit, 2.5)
    clock.unschedule(increment_timer)
    music.stop()
    clock.schedule_unique(game_win_sound, sounds.low_health.get_length())


def game_over():
    global over
    over = True
    clock.schedule_unique(quit, 2.5)
    clock.unschedule(increment_timer)
    music.stop()
    clock.schedule_unique(game_over_sound, sounds.low_health.get_length())


def game_over_sound():
    if buttons_music_game.stop_sound:
        sounds.game_over.play()


def game_win_sound():
    if buttons_music_game.stop_sound:
        sounds.hero.play()


platforms = build("level_zero_platforms.csv", TILE_SIZE)
obstacles = build("level_zero_obstacles.csv", TILE_SIZE)
moneys = build("level_zero_money.csv", TILE_SIZE)
ladders = build("level_zero_ladder.csv", TILE_SIZE)
crystals = build("level_zero_crystal.csv", TILE_SIZE)


def draw():
    if buttons_start_game.start_game == False:
        screen.clear()
        screen.fill("skyblue")
        buttons_start_game.draw()
        if buttons_music_game.stop_sound == True:
            buttons_music_game.draw()
        else:
            buttons_sound_game.draw()

        buttons_quit_game.draw()
    elif buttons_start_game.start_game == True:
        global over, win
        screen.clear()
        screen.fill("skyblue")
        buttons_start_game.y = 400
        buttons_music_game.y = 400
        buttons_quit_game.y = 400

        if over:
            screen.draw.text("Game Over!", center=(WIDTH / 2, HEIGHT / 2))
        elif win:
            screen.draw.text("You Win!", center=(WIDTH / 2, HEIGHT / 2))

        for platform in platforms:
            platform.draw()

        for obstacle in obstacles:
            obstacle.draw()

        for money in moneys:
            money.draw()

        for ladder in ladders:
            ladder.draw()

        for crystal in crystals:
            crystal.draw()

        if player.alive:
            player.draw()

        enemys1.draw()
        enemys2.draw()


def up_enemy1():
    global enemys1_x_speed
    enemys1.x -= enemys1_x_speed
    enemys1.flip_x = True
    if (enemys1.x >= WIDTH - 40) or (enemys1.x <= 40):
        enemys1_x_speed *= -1
        enemys1.flip_x = False


def up_enemy2():
    global enemys2_x_speed
    enemys2.x -= enemys2_x_speed
    enemys2.flip_x = False
    if (enemys2.x >= WIDTH - 70) or (enemys2.x <= 20):
        enemys2_x_speed *= -1
        enemys2.flip_x = True


def update():
    global over, win
    up_enemy1()
    up_enemy2()

    if keyboard.LEFT and player.left > 0:
        player.x -= player.velocity_x
        player.sprite = tree_walk
        player.flip_x = True
        if player.collidelist(platforms) != -1:
            collided = platforms[player.collidelist(platforms)]
            player.x = collided.x + (collided.height / 2 + player.width / 2)
    elif keyboard.RIGHT and player.right < WIDTH:
        player.x += player.velocity_x
        player.sprite = tree_walk
        player.flip_x = False
        if player.collidelist(platforms) != -1:
            collided = platforms[player.collidelist(platforms)]
            player.x = collided.x - (collided.height / 2 + player.width / 2)
    elif keyboard.UP and player.top > 0:
        player.y -= player.velocity_y
        if player.collidelist(ladders) != -1:
            collided = ladders[player.collidelist(ladders)]
            player.y = collided.y - (collided.height / 2 + player.width / 2)

    player.y += player.velocity_y
    player.velocity_y += gravity
    if player.collidelist(platforms) != -1:
        collided = platforms[player.collidelist(platforms)]
        if player.velocity_y >= 0:
            player.bottom = collided.top
            player.jumping = False
        else:
            player.top = collided.bottom

        player.velocity_y = 0

    if player.collidelist(obstacles) != -1:
        player.alive = False
        game_over()

    for enemy in enemys1:
        if player.colliderect(enemys1):
            player.alive = False
            game_over()

    for enemy in enemys2:
        if player.colliderect(enemys2):
            player.alive = False
            game_over()

    for money in moneys:
        if player.colliderect(money):
            if buttons_music_game.stop_sound:
                sounds.money.play()
            moneys.remove(money)

    for crystal in crystals:
        if player.colliderect(crystal):
            if buttons_music_game.stop_sound:
                sounds.money.play()
            crystals.remove(crystal)
            win = True
            game_win()


def on_key_down(key):
    player.sound_visible = True
    if key == keys.SPACE and not player.jumping:
        if buttons_music_game.stop_sound:
            sounds.jump.play()
        player.velocity_y = jump_velocity
        player.jumping = True


def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT:
        player.sprite = tree_stand


start()
pgzrun.go()

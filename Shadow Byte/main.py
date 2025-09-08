import pgzrun
import random

from pgzero.actor import Actor
from pygame import Rect
from menu import create_menu

# Configurações da janela
WIDTH = 800
HEIGHT = 480
TITLE = "Shadow Byte: Escape do Subterrâneo"

# Estados do jogo
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game_over'
current_state = STATE_MENU

# Som e música
music_on = True

player = Actor('byte_idle1', (100, HEIGHT - 150))
player.vx = 0
player.vy = 0
player.on_ground = False
player.direction = 'right'
player.anim_timer = 0
player.anim_state = 'idle'

idle_frames = ['byte_idle1', 'byte_idle2']
walk_frames = ['byte_walk1', 'byte_walk2']
jump_frame = 'byte_jump'

# Plataformas fixas
platforms = [
    Rect((0, HEIGHT - 40), (WIDTH, 40)),
    Rect((200, 380), (120, 20)),
    Rect((400, 300), (120, 20)),
    Rect((600, 220), (120, 20)),
]

# Inimigos
class Enemy:
    def __init__(self, x, y):
        self.actor = Actor('enemy_walk1', (x, y))
        self.vx = random.choice([-1, 1]) * 1
        self.anim_timer = 0
        self.frame = 0

    def update(self):
        self.actor.x += self.vx
        if self.actor.left < 0 or self.actor.right > WIDTH:
            self.vx *= -1
        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.frame = (self.frame + 1) % 2
            self.actor.image = f'enemy_walk{self.frame + 1}'
            self.anim_timer = 0

enemies = [Enemy(300, 260), Enemy(600, 200)]

# Botões do menu importados do módulo
menu_buttons = create_menu(lambda: start_game(), lambda: toggle_sound(), lambda: exit())

def toggle_sound():
    global music_on
    music_on = not music_on
    if music_on:
        music.play('bg_music')
    else:
        music.stop()

def start_game():
    global current_state, player
    current_state = STATE_PLAYING
    player.x, player.y = 100, HEIGHT - 150
    player.vy = 0
    player.on_ground = False
    if music_on:
        music.play('bg_music')

def update():
    if current_state == STATE_PLAYING:
        update_game()
    for e in enemies:
        e.update()

def update_game():
    handle_input()
    apply_gravity()
    check_collisions()
    update_animation()

def handle_input():
    player.vx = 0
    if keyboard.left:
        player.vx = -3
        player.direction = 'left'
    if keyboard.right:
        player.vx = 3
        player.direction = 'right'
    if keyboard.space and player.on_ground:
        player.vy = -10
        player.on_ground = False
        sounds.jump.play()
    player.x += player.vx

def apply_gravity():
    player.vy += 0.5
    player.y += player.vy

def check_collisions():
    player.on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and player.vy >= 0:
            player.y = plat.top
            player.vy = 0
            player.on_ground = True

    for e in enemies:
        if player.colliderect(e.actor):
            game_over()

def game_over():
    global current_state
    current_state = STATE_GAME_OVER
    music.stop()
    sounds.hit.play()

def update_animation():
    player.anim_timer += 1
    if not player.on_ground:
        player.image = jump_frame
    elif player.vx != 0:
        if player.anim_timer >= 10:
            idx = (walk_frames.index(player.image) + 1) % len(walk_frames) if player.image in walk_frames else 0
            player.image = walk_frames[idx]
            player.anim_timer = 0
    else:
        if player.anim_timer >= 20:
            idx = (idle_frames.index(player.image) + 1) % len(idle_frames) if player.image in idle_frames else 0
            player.image = idle_frames[idx]
            player.anim_timer = 0

def draw():
    screen.clear()
    if current_state == STATE_MENU:
        draw_menu()
    elif current_state == STATE_PLAYING:
        draw_game()
    elif current_state == STATE_GAME_OVER:
        draw_game()
        screen.draw.text("Game Over!", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")

def draw_game():
    screen.blit("background", (0, 0))  # background.png
    for plat in platforms:
        screen.draw.filled_rect(plat, "gray")
    player.draw()
    for e in enemies:
        e.actor.draw()

def draw_menu():
    screen.fill("black")
    screen.draw.text(TITLE, center=(WIDTH//2, 80), fontsize=48, color="white")
    for btn in menu_buttons:
        btn.draw(screen)

def on_mouse_down(pos):
    if current_state == STATE_MENU:
        for btn in menu_buttons:
            btn.check_click(pos)

pgzrun.go()
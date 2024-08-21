import pgzrun
import random

WIDTH = 800
HEIGHT = 600


menu_active = True
music_on = False
game_active = False
result_active = False

bullets = []
enemies = []
enemy_bullets = []

score = 0

ship = Actor('ship.png', (WIDTH // 2, HEIGHT - 100))
ship.health = 3
ship.blinking = False
ship.blink_timer = 0


start_button = Actor('start_game.svg', (WIDTH // 2, HEIGHT - 200))
music_button = Actor('off_music.svg', (WIDTH // 2, HEIGHT - 150))
exit_button = Actor('button_exit.svg', (WIDTH // 2, HEIGHT - 100))
restart_button = Actor('restart_button.png', (WIDTH // 2, HEIGHT - 200))


background = Actor('background.png', (WIDTH // 2, HEIGHT // 2))

class Enemy:
    def __init__(self, x, y):
        self.actor = Actor('enemy.png', (x, y))
        self.hits = 2
        self.can_shoot = True
        self.exploding = False
        self.explode_frame = 0
        self.explode_timer = 0
        self.explode_images = ['des2.png', 'des3.png', 'destroyer1.png']

    def update(self):
        if self.exploding:
            self.explode_timer += 1
            if self.explode_timer % 8 == 0:
                self.explode_frame += 1
                if self.explode_frame < len(self.explode_images):
                    self.actor.image = self.explode_images[self.explode_frame]
                else:
                    return True  
        else:
            if self.actor.y < 150:
                self.actor.y += 2
            else:
                if self.can_shoot:
                    shoot_enemy_bullet(self)
                    self.can_shoot = False
        return False

def draw():
    screen.clear()
    if menu_active:
        draw_menu()
    elif game_active:
        draw_game()
    elif result_active:
        draw_result()

def draw_game():
    background.draw()
    ship.draw()
    for bullet in bullets:
        bullet.draw()
    for bullet in enemy_bullets:
        bullet.draw()
    for enemy in enemies:
        enemy.actor.draw()

def draw_result():
    global score
    screen.draw.text(f"Ты заработал {score}", center=(WIDTH // 2, 100), color='white')
    restart_button.draw()

def draw_menu():
    screen.draw.text("Star_viking", center=(400, 100), fontsize=60, color="white")
    start_button.draw()
    music_button.draw()
    exit_button.draw()

def on_mouse_down(pos):
    global menu_active, music_on, game_active
    if menu_active:
        if start_button.collidepoint(pos):
            start_game()
        elif music_button.collidepoint(pos):
            toggle_music()
        elif exit_button.collidepoint(pos):
            exit_game()
    elif result_active:
        if restart_button.collidepoint(pos):
            start_game()

def on_key_down(key):
    if game_active:
        if key == keys.SPACE:
            shoot()

def start_game():
    global menu_active, game_active, result_active, score, bullets, enemies, enemy_bullets
    menu_active = False
    result_active = False
    game_active = True
    ship.health = 3
    ship.blinking = False
    ship.blink_timer = 0
    score = 0
    bullets.clear()
    enemies.clear()
    enemy_bullets.clear()
    ship.pos = (WIDTH // 2, HEIGHT - 100)
    spawn_enemy()

def toggle_music():
    global music_on
    if music_on == True:
        music_button.image = 'off_music.svg'
        music_on = False
        music.stop()
    else:
        music_button.image = 'button_on_music.svg'
        music_on = True
        music.play('music_background')

def exit_game():
    quit()

def update_ship():
    if keyboard.left or keyboard[keys.A]:
        ship.x -= 5
    if keyboard.right or keyboard[keys.D]:
        ship.x += 5
    if keyboard.up or keyboard[keys.W]:
        ship.y -= 5
    if keyboard.down or keyboard[keys.S]:
        ship.y += 5

    if ship.blinking:
        ship.blink_timer += 1
        if ship.blink_timer % 20 < 10:
            ship.image = 'red_ship.png'
        else:
            ship.image = 'ship.png'

        if ship.blink_timer >= 60:
            ship.blinking = False
            ship.blink_timer = 0
            ship.image = 'ship.png'

def update_bullets():
    for bullet in bullets:
        bullet.y -= 10
        if bullet.y < 0:
            bullets.remove(bullet)

def update_enemy_bullets():
    for bullet in enemy_bullets:
        bullet.y += 5
        if bullet.y > HEIGHT:
            enemy_bullets.remove(bullet)

def update_enemies():
    for enemy in enemies[:]:
        if enemy.update():
            enemies.remove(enemy)

def shoot():
    bullet = Actor('bull.png', (ship.x, ship.y - 50))
    bullets.append(bullet)

def shoot_enemy_bullet(enemy):
    bullet = Actor('bull.png', (enemy.actor.x, enemy.actor.y + 50))
    enemy_bullets.append(bullet)

def check_collisions():
    global score
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy.actor):
                bullet.y = -10
                enemy.hits -= 1
                if enemy.hits <= 0:
                    enemy.exploding = True
                    score += 10

    for bullet in enemy_bullets[:]:
        if bullet.colliderect(ship):
            enemy_bullets.remove(bullet)
            ship.health -= 1
            ship.blinking = True
            if ship.health <= 0:
                game_over()

def spawn_enemy():
    x = random.randint(50, WIDTH - 50)
    enemy = Enemy(x, -50)
    enemies.append(enemy)

def update():
    if game_active:
        update_ship()
        update_bullets()
        update_enemy_bullets()
        update_enemies()
        check_collisions()

        
        if len(enemies) < 3:  
            if random.randint(0, 50) == 0:  
                spawn_enemy()

def game_over():
    global game_active, result_active
    game_active = False
    result_active = True
    
    

pgzrun.go()
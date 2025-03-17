import tkinter as tk
import random
import os

# Default game settings (some values remain fixed, even if the screen size changes)
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 30
PLAYER_SPEED = 5
BULLET_SPEED = 20
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 30
ENEMY_ROWS, ENEMY_COLS = 3, 8
ENEMY_PADDING = 20
BASE_ENEMY_SPEED = 5

HIGHSCORE_FILE = "highscore.txt"

# Global game state variables
level = 1
score = 0
enemies = []
bullets = []
powerups = []  # neue Liste für Powerups
enemy_direction = 1  # 1 for right, -1 for left
enemy_speed = BASE_ENEMY_SPEED
paused = False

# Spielerbewegungsflags
move_left = False
move_right = False

# Globale Variablen für Spieler
player = None
player_x = None
player_y = None

menu_items = []
pause_menu_items = []

# ---- New global variables for key configuration ----
KEY_MOVE_LEFT = "Left"
KEY_MOVE_RIGHT = "Right"
KEY_FIRE = "space"
KEY_PAUSE = "p"

# Zusätzliche globale Variablen für Powerup-Effekte
default_player_speed = PLAYER_SPEED
shield_active = False
score_multiplier = 1
powerup_effects = ["Astro Boost", "Galactic Shield", "Cosmic Chaos"]

# ---------- Initialize window and canvas ----------
root = tk.Tk()
root.title("Space Invaders")
root.attributes("-fullscreen", True)
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

score_text = None

# ---------- Highscore Functions ----------
def read_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
        except:
            return 0
    return 0

def update_highscore(final_score):
    highscore = read_highscore()
    if final_score > highscore:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(final_score))
        return final_score
    return highscore

# ---------- Background: Sternenhimmel ----------
def draw_starfield():
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        r = random.randint(1, 2)
        canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="", tag="star")
    canvas.tag_lower("star")

# ---------- Game Functions ----------
def setup_enemies():
    global enemies, enemy_direction
    enemies = []
    enemy_direction = 1
    start_x = ENEMY_PADDING
    start_y = ENEMY_PADDING
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            x1 = start_x + col * (ENEMY_WIDTH + ENEMY_PADDING)
            y1 = start_y + row * (ENEMY_HEIGHT + ENEMY_PADDING)
            enemy = canvas.create_rectangle(x1, y1, x1 + ENEMY_WIDTH, y1 + ENEMY_HEIGHT, fill="orange", outline="gold", width=2)
            enemies.append(enemy)

def update_status_text():
    global score_text
    canvas.itemconfig(score_text, text=f"Score: {score}  Level: {level}")
    root.title(f"Space Invaders - Level: {level}")

def move_player(dx):
    coords = canvas.bbox(player)
    if not coords or len(coords) < 4:
        return
    x1, y1, x2, y2 = coords
    if (dx < 0 and x1 + dx >= 0) or (dx > 0 and x2 + dx <= WIDTH):
        canvas.move(player, dx, 0)

def update_player():
    if move_left:
        move_player(-PLAYER_SPEED)
    if move_right:
        move_player(PLAYER_SPEED)

def fire_bullet(_event=None):
    coords = canvas.bbox(player)
    if not coords or len(coords) < 4:
        return
    x1, y1, x2, _ = coords
    cx = (x1 + x2) // 2
    bullet = canvas.create_oval(cx - 3, y1 - 10, cx + 3, y1, fill="cyan", outline="white")
    bullets.append(bullet)

def update_bullets():
    global score
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -BULLET_SPEED)
        coords = canvas.coords(bullet)
        if len(coords) < 4:
            continue
        bx1, by1, bx2, by2 = coords
        if by2 < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
        else:
            overlapping = canvas.find_overlapping(bx1, by1, bx2, by2)
            for item in overlapping:
                if item in enemies:
                    canvas.delete(item)
                    if item in enemies:
                        enemies.remove(item)
                    # 20% Chance, dass ein Powerup droppt
                    if random.random() < 0.2:
                        ex1, ey1, ex2, ey2 = canvas.coords(item)
                        cx = (ex1 + ex2) // 2
                        cy = (ey1 + ey2) // 2
                        effect = random.choice(powerup_effects)
                        pu = canvas.create_oval(cx - 10, cy - 10, cx + 10, cy + 10, fill="magenta", outline="white", width=2, tag="powerup")
                        # Optional: Schreibe den Effekt-Namen in der Mitte
                        canvas.create_text(cx, cy, text=effect.split()[0], fill="white", font=("Helvetica", 8), tag="powerup")
                        powerups.append({"id": pu, "effect": effect})
                    canvas.delete(bullet)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    score += 10 * score_multiplier
                    update_status_text()
                    break

def update_enemies():
    global enemy_direction, enemy_speed
    move_side = enemy_speed * enemy_direction
    hit_edge = False
    for enemy in enemies:
        ex1, _, ex2, _ = canvas.coords(enemy)
        if ex1 + move_side < 0 or ex2 + move_side > WIDTH:
            hit_edge = True
            break

    if hit_edge:
        enemy_direction *= -1
        for enemy in enemies:
            canvas.move(enemy, 0, ENEMY_HEIGHT // 2)
    else:
        for enemy in enemies:
            canvas.move(enemy, move_side, 0)

def update_powerups():
    global powerups
    for pu in powerups[:]:
        # Powerup nach unten bewegen
        canvas.move(pu["id"], 0, 5)
        # Hole aktuelle Position
        pu_coords = canvas.bbox(pu["id"])
        if not pu_coords or len(pu_coords) < 4:
            powerups.remove(pu)
            continue
        _, pu_y1, _, pu_y2 = pu_coords
        if pu_y1 > HEIGHT:
            canvas.delete(pu["id"])
            powerups.remove(pu)
            continue
        # Kollision mit Spieler prüfen
        player_coords = canvas.bbox(player)
        if player_coords and canvas.bbox_overlap(player_coords, pu_coords):
            apply_powerup(pu["effect"])
            canvas.delete(pu["id"])
            powerups.remove(pu)

# Hilfsfunktion zum Prüfen der Überlappung zweier Boxen
def bbox_overlap(b1, b2):
    return not (b1[2] < b2[0] or b1[0] > b2[2] or b1[3] < b2[1] or b1[1] > b2[3])
# Wir fügen bbox_overlap der Canvas als Methode hinzu, da sie in update_powerups genutzt wird.
canvas.bbox_overlap = bbox_overlap

def apply_powerup(effect):
    global PLAYER_SPEED, shield_active, score_multiplier
    message_id = canvas.create_text(WIDTH//2, HEIGHT//2, text=f"{effect} aktiviert!", fill="white", font=("Helvetica", 32))
    canvas.after(2000, lambda: canvas.delete(message_id))
    if effect == "Astro Boost":
        PLAYER_SPEED += 3
        canvas.after(5000, revert_astro_boost)
    elif effect == "Galactic Shield":
        shield_active = True
        canvas.after(5000, revert_shield)
    elif effect == "Cosmic Chaos":
        score_multiplier = 2
        canvas.after(5000, revert_chaos)

def revert_astro_boost():
    global PLAYER_SPEED
    PLAYER_SPEED = default_player_speed

def revert_shield():
    global shield_active
    shield_active = False

def revert_chaos():

    global score
    # Falls ein Schild aktiv ist, wird Game Over vorübergehend verhindert.
    if shield_active:
        return False
    for enemy in enemies:
        enemy_coords = canvas.coords(enemy)
        if not enemy_coords or len(enemy_coords) < 4:
            continue
        _, ey1, _, ey2 = enemy_coords
        if ey2 >= player_y:
            canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER", fill="white", font=("Arial", 48))
            high = update_highscore(score)
            canvas.create_text(WIDTH // 2, HEIGHT // 2 + 60, text=f"Highscore: {high}", fill="white", font=("Arial", 24))
            return True
    return False
def new_level():
    global level, enemy_speed
    level += 1
    enemy_speed = BASE_ENEMY_SPEED + (level - 1) * 2
    update_status_text()
    setup_enemies()
    new_bg = random.choice(["black", "midnightblue", "navy"])
    canvas.config(bg=new_bg)
    draw_starfield()

def game_loop():
    if paused:
        return
    update_player()
    update_bullets()
    update_enemies()
    update_powerups()
def pause_game(_event=None):
        if not enemies:
            new_level()
        root.after(50, game_loop)

# ---------- Pause Menu Functions ----------
def pause_game(event=None):
    global paused, pause_menu_items
    if paused:
        return
def pause_game(event=None):
    global paused, pause_menu_items
    if paused:
        return
    paused = True
    overlay = canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black", stipple="gray50")
    text = canvas.create_text(WIDTH // 2, HEIGHT // 3, text="PAUSED", fill="white", font=("Helvetica", 48, "bold"))
    resume_rect = canvas.create_rectangle(WIDTH // 2 - 100, HEIGHT // 2, WIDTH // 2 + 100, HEIGHT // 2 + 50, fill="gray")
    resume_text = canvas.create_text(WIDTH // 2, HEIGHT // 2 + 25, text="Resume", fill="white", font=("Helvetica", 24))
    main_rect = canvas.create_rectangle(WIDTH // 2 - 100, HEIGHT // 2 + 70, WIDTH // 2 + 100, HEIGHT // 2 + 120, fill="gray")
    main_text = canvas.create_text(WIDTH // 2, HEIGHT // 2 + 95, text="Main Menu", fill="white", font=("Helvetica", 24))
    pause_menu_items = [overlay, text, resume_rect, resume_text, main_rect, main_text]
    canvas.tag_bind(resume_rect, "<Button-1>", lambda _: resume_game())
    canvas.tag_bind(resume_text, "<Button-1>", lambda _: resume_game())
    canvas.tag_bind(main_rect, "<Button-1>", lambda _: show_menu())
    canvas.tag_bind(main_text, "<Button-1>", lambda _: show_menu())

def resume_game(event=None):
    global paused, pause_menu_items
    paused = False
    for item in pause_menu_items:
        canvas.delete(item)
    pause_menu_items.clear()
    game_loop()
    for item in pause_menu_items:
        canvas.delete(item)
    pause_menu_items.clear()
    game_loop()

# ---------- Settings Menu Functions ----------
player_speed_scale = None
bullet_speed_scale = None

# Neue globale Variablen für Key-Entry-Widgets
key_left_entry = None
key_right_entry = None
key_fire_entry = None
key_pause_entry = None

def save_settings():
    global PLAYER_SPEED, BULLET_SPEED, player_speed_scale, bullet_speed_scale
    global KEY_MOVE_LEFT, KEY_MOVE_RIGHT, KEY_FIRE, KEY_PAUSE
    try:
        PLAYER_SPEED = int(player_speed_scale.get())
        BULLET_SPEED = int(bullet_speed_scale.get())
    except:
        pass
    # Update key configuration
def show_settings():
    canvas.delete("all")
    draw_starfield()
    _settings_title = canvas.create_text(WIDTH // 2, 80, text="Einstellungen", fill="white", font=("Helvetica", 48, "bold"))
    
    # Speed settings
    global player_speed_scale, bullet_speed_scale, key_left_entry, key_right_entry, key_fire_entry, key_pause_entry
    player_speed_scale = tk.Scale(root, from_=1, to=20, orient="horizontal", label="Spielgeschwindigkeit", bg="black", fg="white", highlightbackground="black", troughcolor="gray")
    player_speed_scale.set(PLAYER_SPEED)
    bullet_speed_scale = tk.Scale(root, from_=10, to=50, orient="horizontal", label="Schussgeschwindigkeit", bg="black", fg="white", highlightbackground="black", troughcolor="gray")
    bullet_speed_scale.set(BULLET_SPEED)
    canvas.create_window(WIDTH // 2, 150, window=player_speed_scale)
    canvas.create_window(WIDTH // 2, 200, window=bullet_speed_scale)
    player_speed_scale = tk.Scale(root, from_=1, to=20, orient="horizontal", label="Spielgeschwindigkeit", bg="black", fg="white", highlightbackground="black", troughcolor="gray")
    player_speed_scale.set(PLAYER_SPEED)
    bullet_speed_scale = tk.Scale(root, from_=10, to=50, orient="horizontal", label="Schussgeschwindigkeit", bg="black", fg="white", highlightbackground="black", troughcolor="gray")
    bullet_speed_scale.set(BULLET_SPEED)
    ps_window = canvas.create_window(WIDTH // 2, 150, window=player_speed_scale)
    bs_window = canvas.create_window(WIDTH // 2, 200, window=bullet_speed_scale)
    
    # Control settings
    canvas.create_text(WIDTH // 2, 250, text="Steuerung", fill="white", font=("Helvetica", 24, "bold"))
    canvas.create_text(WIDTH // 2 - 60, 290, text="Links:", fill="white", font=("Helvetica", 16))
    key_left_entry = tk.Entry(root, width=5, justify="center")
    key_left_entry.insert(0, KEY_MOVE_LEFT)
    canvas.create_window(WIDTH // 2 + 40, 290, window=key_left_entry)
    
    canvas.create_text(WIDTH // 2 - 60, 330, text="Rechts:", fill="white", font=("Helvetica", 16))
    key_right_entry = tk.Entry(root, width=5, justify="center")
    key_right_entry.insert(0, KEY_MOVE_RIGHT)
    canvas.create_window(WIDTH // 2 + 40, 330, window=key_right_entry)
    
    canvas.create_text(WIDTH // 2 - 60, 370, text="Schuss:", fill="white", font=("Helvetica", 16))
    key_fire_entry = tk.Entry(root, width=5, justify="center")
    key_fire_entry.insert(0, KEY_FIRE)
    canvas.create_window(WIDTH // 2 + 40, 370, window=key_fire_entry)
    
    canvas.create_text(WIDTH // 2 - 60, 410, text="Pause:", fill="white", font=("Helvetica", 16))
    key_pause_entry = tk.Entry(root, width=5, justify="center")
    key_pause_entry.insert(0, KEY_PAUSE)
    canvas.create_window(WIDTH // 2 + 40, 410, window=key_pause_entry)
    
    save_rect = canvas.create_rectangle(WIDTH // 2 - 100, 450, WIDTH // 2 + 100, 500, fill="gray")
    save_text = canvas.create_text(WIDTH // 2, 475, text="SAVE", fill="white", font=("Helvetica", 24, "bold"))
    back_rect = canvas.create_rectangle(WIDTH // 2 - 100, 510, WIDTH // 2 + 100, 560, fill="gray")
    back_text = canvas.create_text(WIDTH // 2, 535, text="Back", fill="white", font=("Helvetica", 24, "bold"))
    
def show_menu():
    global menu_items, score, level, enemy_speed, move_left, move_right, player, player_y, bullets
    canvas.delete("all")
    menu_items = []
    highscore = read_highscore()
    bg_rect = canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black")
    draw_starfield()
    _menu_title = canvas.create_text(WIDTH // 2, HEIGHT // 4, text="Space Invaders", fill="white", font=("Helvetica", 56, "bold"))
    hs_text = canvas.create_text(WIDTH // 2, HEIGHT // 4 + 70, text=f"Highscore: {highscore}", fill="yellow", font=("Helvetica", 24))
    
    start_rect = canvas.create_rectangle(WIDTH // 2 - 100, HEIGHT // 2 - 40, WIDTH // 2 + 100, HEIGHT // 2, fill="gray")
    start_text = canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, text="START", fill="white", font=("Helvetica", 24, "bold"))
    draw_starfield()
    title = canvas.create_text(WIDTH // 2, HEIGHT // 4, text="Space Invaders", fill="white", font=("Helvetica", 56, "bold"))
    hs_text = canvas.create_text(WIDTH // 2, HEIGHT // 4 + 70, text=f"Highscore: {highscore}", fill="yellow", font=("Helvetica", 24))
    
    start_rect = canvas.create_rectangle(WIDTH // 2 - 100, HEIGHT // 2 - 40, WIDTH // 2 + 100, HEIGHT // 2, fill="gray")
    start_text = canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, text="START", fill="white", font=("Helvetica", 24, "bold"))
    
    settings_rect = canvas.create_rectangle(WIDTH // 2 - 100, HEIGHT // 2 + 20, WIDTH // 2 + 100, HEIGHT // 2 + 60, fill="gray")
    settings_text = canvas.create_text(WIDTH // 2, HEIGHT // 2 + 40, text="EINSTELLUNGEN", fill="white", font=("Helvetica", 16, "bold"))
    
    quit_rect = canvas.create_rectangle(WIDTH // 2 - 100, HEIGHT // 2 + 80, WIDTH // 2 + 100, HEIGHT // 2 + 120, fill="gray")
    quit_text = canvas.create_text(WIDTH // 2, HEIGHT // 2 + 100, text="VERLASSEN", fill="white", font=("Helvetica", 24, "bold"))
    
    menu_items.extend([bg_rect, title, hs_text, start_rect, start_text, settings_rect, settings_text, quit_rect, quit_text])
    canvas.tag_bind(start_rect, "<Button-1>", start_game)
    canvas.tag_bind(start_text, "<Button-1>", start_game)
    canvas.tag_bind(settings_rect, "<Button-1>", lambda _: show_settings())
    canvas.tag_bind(settings_text, "<Button-1>", lambda _: show_settings())
    canvas.tag_bind(quit_rect, "<Button-1>", lambda _: root.destroy())
    canvas.tag_bind(quit_text, "<Button-1>", lambda _: root.destroy())
    root.bind("<Return>", start_game)
    canvas.focus_set()

# ---------- Input Handlers ----------
def on_key_press(event):
    global move_left, move_right
    ek = event.keysym.lower()
    if ek == KEY_MOVE_LEFT.lower():
        move_left = True
    elif ek == KEY_MOVE_RIGHT.lower():
        move_right = True
    elif ek == KEY_FIRE.lower():
        fire_bullet()
    elif ek == KEY_PAUSE.lower():
        pause_game()

def on_key_release(event):
    global move_left, move_right
    ek = event.keysym.lower()
    if ek == KEY_MOVE_LEFT.lower():
        move_left = False
    elif ek == KEY_MOVE_RIGHT.lower():
        move_right = False

# ---------- Game Start ----------
def start_game(event=None):
    global player, score_text, menu_items, level, score, enemy_speed, move_left, move_right, player_x, player_y, bullets, paused
    for item in menu_items:
        canvas.delete(item)
    menu_items.clear()
    
    level = 1
    score = 0
    enemy_speed = BASE_ENEMY_SPEED
    move_left = False
    move_right = False
    bullets = []
    paused = False
    canvas.config(bg="black")
    canvas.delete("all")
    draw_starfield()
    
    pause_btn = canvas.create_rectangle(WIDTH - 80, 10, WIDTH - 10, 40, fill="gray")
    pause_txt = canvas.create_text(WIDTH - 45, 25, text="Pause", fill="white", font=("Helvetica", 12, "bold"))
    canvas.tag_bind(pause_btn, "<Button-1>", pause_game)
    canvas.tag_bind(pause_txt, "<Button-1>", pause_game)
    
    score_text = canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}  Level: {level}", fill="white", font=("Helvetica", 16, "bold"))
    
    player_x = (WIDTH - PLAYER_WIDTH) // 2
    player_y = HEIGHT - PLAYER_HEIGHT - 10
    player = canvas.create_polygon(
        player_x + PLAYER_WIDTH // 2, player_y,
        player_x, player_y + PLAYER_HEIGHT,
        player_x + PLAYER_WIDTH, player_y + PLAYER_HEIGHT,
        fill="cyan", outline="white", width=2
    )
    setup_enemies()
    update_status_text()
    canvas.focus_set()
    game_loop()

root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

show_menu()
root.mainloop()

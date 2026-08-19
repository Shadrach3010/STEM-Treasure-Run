import pygame
import random
import os
import math
import wave
import struct

# Function to ensure chiptune audio assets exist by synthesizing them offline
def ensure_assets():
    base_dir = "assets"
    os.makedirs(base_dir, exist_ok=True)
    
    music_path = os.path.join(base_dir, "bg_music.wav")
    coin_path = os.path.join(base_dir, "coin.wav")
    hit_path = os.path.join(base_dir, "hit.wav")
    powerup_path = os.path.join(base_dir, "powerup.wav")
    rocket_launch_path = os.path.join(base_dir, "rocket_launch.wav")
    explosion_path = os.path.join(base_dir, "explosion.wav")
    heal_path = os.path.join(base_dir, "heal.wav")
    
    # Simple software synthesizer to generate 8-bit sound effects & music
    def generate_sound(filename, duration, type_sound):
        if os.path.exists(filename):
            return
        sample_rate = 22050
        num_samples = int(sample_rate * duration)
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)   # 16-bit
            wav_file.setframerate(sample_rate)
            frames = bytearray()
            
            for i in range(num_samples):
                t = i / sample_rate
                if type_sound == 'music':
                    # Catchy 8-bit looping chiptune chord progression (C - G - Am - F)
                    melody = [
                        261.63, 329.63, 392.00, 329.63,  # C major
                        392.00, 493.88, 587.33, 493.88,  # G major
                        440.00, 523.25, 659.25, 523.25,  # A minor
                        349.23, 440.00, 523.25, 440.00   # F major
                    ]
                    note_idx = int(t * 2) % len(melody)
                    freq = melody[note_idx]
                    note_time = t % 0.5
                    decay = math.exp(-4.0 * note_time)
                    
                    # Triangle-like wave for retro feel
                    val = (2.0 * abs(2.0 * ((t * freq) % 1.0) - 1.0) - 1.0) * 0.25
                    # Sub-bass sine wave layer
                    bass_freq = melody[(note_idx // 4) * 4] / 2.0
                    val += math.sin(2.0 * math.pi * bass_freq * t) * 0.2
                    val *= decay
                elif type_sound == 'coin':
                    # Classic 8-bit upward sweep coin sound
                    freq = 600.0 + (t / duration) * 600.0
                    val = 0.2 if ((t * freq) % 1.0) < 0.5 else -0.2
                    decay = math.exp(-3.0 * t)
                    val *= decay
                elif type_sound == 'hit':
                    # Heavy downward sweep explosion noise for hit sound
                    freq = 180.0 - (t / duration) * 140.0
                    import random as rnd
                    noise = (rnd.random() * 2.0 - 1.0) * 0.12
                    val = math.sin(2.0 * math.pi * freq * t) * 0.25 + noise
                    decay = math.exp(-6.0 * t)
                    val *= decay
                elif type_sound == 'powerup':
                    # Arpeggio upward sweep
                    notes = [659.25, 783.99, 987.77, 1318.51]
                    note_idx = min(int(t / (duration / len(notes))), len(notes) - 1)
                    freq = notes[note_idx]
                    val = 0.2 if ((t * freq) % 1.0) < 0.5 else -0.2
                    decay = math.exp(-2.0 * t)
                    val *= decay
                elif type_sound == 'rocket_launch':
                    # Upward sweep white-noise like sound
                    import random as rnd
                    noise = (rnd.random() * 2.0 - 1.0) * 0.2
                    freq = 200.0 + (t / duration) * 600.0
                    val = math.sin(2.0 * math.pi * freq * t) * noise
                    decay = math.exp(-2.5 * t)
                    val *= decay
                elif type_sound == 'explosion':
                    # Heavy rumble noise decay
                    import random as rnd
                    noise = (rnd.random() * 2.0 - 1.0) * 0.35
                    freq = 130.0 - (t / duration) * 100.0
                    val = math.sin(2.0 * math.pi * freq * t) * 0.2 + noise
                    decay = math.exp(-4.5 * t)
                    val *= decay
                elif type_sound == 'heal':
                    # Quick two-tone high pitch chime
                    notes = [1046.50, 1567.98]
                    note_idx = 0 if t < (duration * 0.4) else 1
                    freq = notes[note_idx]
                    val = math.sin(2.0 * math.pi * freq * t) * 0.25
                    decay = math.exp(-3.0 * t)
                    val *= decay
                else:
                    val = 0
                
                val = max(-1.0, min(1.0, val))
                sample = int(val * 32767)
                frames.extend(struct.pack('<h', sample))
            wav_file.writeframes(frames)

    generate_sound(music_path, 8.0, 'music')
    generate_sound(coin_path, 0.15, 'coin')
    generate_sound(hit_path, 0.3, 'hit')
    generate_sound(powerup_path, 0.32, 'powerup')
    generate_sound(rocket_launch_path, 0.3, 'rocket_launch')
    generate_sound(explosion_path, 0.5, 'explosion')
    generate_sound(heal_path, 0.3, 'heal')

# Initialize Pygame and audio mixer
pygame.init()
pygame.mixer.init()

# Game settings
WIDTH = 800
HEIGHT = 600
FPS = 60

# Sierra Leone-inspired colors
GREEN = (30, 145, 78)
LIGHT_GREEN = (112, 193, 126)
WHITE = (255, 255, 255)
BLUE = (0, 114, 188)
LIGHT_BLUE = (95, 188, 235)
NAVY = (13, 48, 74)
BLACK = (25, 25, 25)
GOLD = (255, 205, 45)
ROCK_GRAY = (103, 110, 116)
ROCK_LIGHT = (155, 162, 168)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STEM Treasure Run")

# Game clock and text styles
clock = pygame.time.Clock()
title_font = pygame.font.Font(None, 48)
hud_font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
message_font = pygame.font.Font(None, 48)

# Load and resize the STEM coin image
coin_image = pygame.image.load(
    "assets/Untitled_design-removebg-preview.png"
).convert_alpha()
coin_image = pygame.transform.smoothscale(coin_image, (58, 58))

# Ensure synthesized sound assets exist
ensure_assets()

# Load music and sounds
pygame.mixer.music.load("assets/bg_music.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)  # Loop forever

coin_sound = pygame.mixer.Sound("assets/coin.wav")
coin_sound.set_volume(0.5)
hit_sound = pygame.mixer.Sound("assets/hit.wav")
hit_sound.set_volume(0.5)

powerup_sound = pygame.mixer.Sound("assets/powerup.wav")
powerup_sound.set_volume(0.5)
rocket_launch_sound = pygame.mixer.Sound("assets/rocket_launch.wav")
rocket_launch_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
explosion_sound.set_volume(0.5)
heal_sound = pygame.mixer.Sound("assets/heal.wav")
heal_sound.set_volume(0.5)

# Initialize Joysticks/Controllers
pygame.joystick.init()
joysticks = {}
for i in range(pygame.joystick.get_count()):
    joy = pygame.joystick.Joystick(i)
    joy.init()
    joysticks[joy.get_instance_id()] = joy

# Player variables
player_x = 380
player_y = 500
player_width = 40
player_height = 50
player_speed = 5
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Score, lives, and game state
score = 0
lives = 3
game_state = "playing"

# Invulnerability state
is_invulnerable = False
invulnerable_timer = 0
INVULNERABLE_DURATION = 1500  # 1.5 seconds

# Powerup, Rocket, and Particle state variables
active_powerups = []
active_rockets = []
particles = []

immunity_active = False
immunity_timer = 0
IMMUNITY_POWERUP_DURATION = 5000  # 5 seconds

booster_active = False
booster_timer = 0
BOOSTER_POWERUP_DURATION = 5000  # 5 seconds
NORMAL_PLAYER_SPEED = 5
BOOSTED_PLAYER_SPEED = 9

rocket_ammo = 0
distance_run = 0.0

powerup_spawn_interval = 8000  # Spawn power-up every 8 seconds
last_powerup_spawn = 0         # Start spawning soon

# Scrolling background state
bg_offset = 0.0
scroll_speed = 3.0

# Initialize background decorations (trees, grass, flowers)
decorations = []
for _ in range(15):
    # Spawn decorations on left or right grass side banks
    side = random.choice(['left', 'right'])
    x = random.randint(10, 170) if side == 'left' else random.randint(620, 770)
    y = random.randint(92, HEIGHT)
    dtype = random.choice(['tree', 'grass', 'flower'])
    decorations.append({
        'x': x,
        'y': y,
        'type': dtype,
        'color': random.choice([(18, 120, 58), (50, 160, 90), (220, 200, 50)]),
        'size': random.randint(8, 16)
    })

# Game dynamic objects
obstacles = []
coins = []

def spawn_safe_rock(other_rocks, other_coins):
    while True:
        # Spawn rock above the header line (y <= -50)
        x = random.randint(100, WIDTH - 180)
        y = random.randint(-200, -50)
        w = random.randint(70, 85)
        h = random.randint(50, 65)
        rect = pygame.Rect(x, y, w, h)
        
        # Ensure no overlap with other rocks or coins
        overlap = False
        for other in other_rocks:
            if rect.colliderect(other):
                overlap = True
                break
        for coin in other_coins:
            if rect.colliderect(coin):
                overlap = True
                break
        if not overlap:
            return rect

def spawn_safe_coin(other_rocks, other_coins):
    while True:
        # Coins spawn mostly on the central roadway (x: 210 to 530)
        x = random.randint(210, 530)
        y = random.randint(-250, -50)
        rect = pygame.Rect(x, y, 58, 58)
        
        # Ensure coins are distant (minimum distance: 120px from rocks, 150px from other coins)
        too_close = False
        for other in other_rocks:
            dist = math.hypot(rect.centerx - other.centerx, rect.centery - other.centery)
            if dist < 120:
                too_close = True
                break
        if too_close:
            continue
            
        for other in other_coins:
            dist = math.hypot(rect.centerx - other.centerx, rect.centery - other.centery)
            if dist < 150:
                too_close = True
                break
        if not too_close:
            return rect

def reset_obstacles_and_coins():
    global obstacles, coins
    obstacles = []
    coins = []
    
    # Distribute initial vertical spacing to ensure continuous but non-clashing flow
    for i in range(3):
        rock = pygame.Rect(
            random.randint(100, WIDTH - 180),
            -100 - i * 180,
            random.randint(70, 85),
            random.randint(50, 65)
        )
        obstacles.append(rock)
        
    for i in range(2):
        coin = pygame.Rect(
            random.randint(210, 530),
            -200 - i * 250,
            58,
            58
        )
        coins.append(coin)

def restart_game():
    global score, lives, game_state, player_x, player_y, is_invulnerable, bg_offset
    global active_powerups, active_rockets, particles
    global immunity_active, immunity_timer, booster_active, booster_timer, rocket_ammo
    global last_powerup_spawn, distance_run
    score = 0
    lives = 3
    game_state = "playing"
    player_x = 380
    player_y = 500
    player_rect.x = player_x
    player_rect.y = player_y
    is_invulnerable = False
    bg_offset = 0.0
    
    # Reset lists
    active_powerups = []
    active_rockets = []
    particles = []
    
    # Reset powerup variables
    immunity_active = False
    immunity_timer = 0
    booster_active = False
    booster_timer = 0
    rocket_ammo = 0
    distance_run = 0.0
    last_powerup_spawn = pygame.time.get_ticks()

    reset_obstacles_and_coins()

# Initial spawn
reset_obstacles_and_coins()

def draw_heart_shape(surface, x, y, size, color):
    # Programmatic heart: two circles for the lobes and a bottom polygon
    left_x = int(x + size * 0.3)
    left_y = int(y + size * 0.3)
    radius = int(size * 0.3)
    pygame.draw.circle(surface, color, (left_x, left_y), radius)
    
    right_x = int(x + size * 0.7)
    right_y = int(y + size * 0.3)
    pygame.draw.circle(surface, color, (right_x, right_y), radius)
    
    points = [
        (int(x + size * 0.05), int(y + size * 0.4)),
        (int(x + size * 0.95), int(y + size * 0.4)),
        (int(x + size * 0.5), int(y + size * 0.95))
    ]
    pygame.draw.polygon(surface, color, points)

def draw_heart(surface, x, y, size, color):
    # Draw outline (dark-gray shadow) then the filled shape
    draw_heart_shape(surface, x - 1, y - 1, size + 2, (15, 15, 15))
    draw_heart_shape(surface, x, y, size, color)

def spawn_safe_powerup(other_rocks, other_coins, existing_powerups):
    while True:
        # Powerups spawn on roadway (x: 210 to 530)
        x = random.randint(210, 530)
        y = random.randint(-250, -50)
        rect = pygame.Rect(x, y, 40, 40)
        
        # Ensure powerups are distant (minimum distance: 120px from rocks, 150px from coins/other powerups)
        too_close = False
        for other in other_rocks:
            dist = math.hypot(rect.centerx - other.centerx, rect.centery - other.centery)
            if dist < 120:
                too_close = True
                break
        if too_close:
            continue
            
        for other in other_coins:
            dist = math.hypot(rect.centerx - other.centerx, rect.centery - other.centery)
            if dist < 150:
                too_close = True
                break
        if too_close:
            continue
            
        for p in existing_powerups:
            other = p['rect']
            dist = math.hypot(rect.centerx - other.centerx, rect.centery - other.centery)
            if dist < 150:
                too_close = True
                break
        if not too_close:
            return rect

def spawn_powerup(powerup_type=None):
    global active_powerups
    if not powerup_type:
        if lives == 1:
            # 50% chance to spawn health, 50% chance for others
            if random.random() < 0.5:
                powerup_type = 'health'
            else:
                powerup_type = random.choice(['immunity', 'booster', 'rocket'])
        else:
            powerup_type = random.choice(['immunity', 'booster', 'rocket'])
            
    rect = spawn_safe_powerup(obstacles, coins, active_powerups)
    active_powerups.append({
        'rect': rect,
        'type': powerup_type
    })

def trigger_health_spawn():
    health_on_screen = any(p['type'] == 'health' for p in active_powerups)
    if not health_on_screen:
        spawn_powerup('health')

def fire_rocket():
    global rocket_ammo
    rocket_ammo -= 1
    # Spawn rocket projectile in front of player
    active_rockets.append(pygame.Rect(player_x + player_width // 2 - 5, player_y - 24, 10, 24))
    rocket_launch_sound.play()

def draw_collectible(surface, p_type, x, y, size):
    center_x = x + size // 2
    center_y = y + size // 2
    radius = size // 2
    
    if p_type == 'immunity':
        # Blue shield collectible
        pygame.draw.circle(surface, NAVY, (center_x, center_y), radius)
        pygame.draw.circle(surface, LIGHT_BLUE, (center_x, center_y), radius - 2, 2)
        shield_pts = [
            (center_x - 8, center_y - 10),
            (center_x + 8, center_y - 10),
            (center_x + 8, center_y),
            (center_x, center_y + 10),
            (center_x - 8, center_y)
        ]
        pygame.draw.polygon(surface, LIGHT_BLUE, shield_pts)
        pygame.draw.polygon(surface, WHITE, shield_pts, 2)
        
    elif p_type == 'booster':
        # Orange/yellow lightning booster
        pygame.draw.circle(surface, NAVY, (center_x, center_y), radius)
        pygame.draw.circle(surface, GOLD, (center_x, center_y), radius - 2, 2)
        bolt_pts = [
            (center_x + 2, center_y - 10),
            (center_x - 6, center_y + 2),
            (center_x, center_y + 2),
            (center_x - 2, center_y + 10),
            (center_x + 6, center_y - 2),
            (center_x, center_y - 2)
        ]
        pygame.draw.polygon(surface, GOLD, bolt_pts)
        
    elif p_type == 'health':
        # Pulsing Red Heart
        pulse = math.sin(pygame.time.get_ticks() * 0.015) * 3
        draw_heart(surface, x - int(pulse//2), y - int(pulse//2), size + int(pulse), (230, 40, 40))
        
    elif p_type == 'rocket':
        # Navy circle with miniature rocket
        pygame.draw.circle(surface, NAVY, (center_x, center_y), radius)
        pygame.draw.circle(surface, WHITE, (center_x, center_y), radius - 2, 2)
        pygame.draw.rect(surface, WHITE, (center_x - 3, center_y - 4, 6, 12))
        pygame.draw.polygon(surface, (230, 40, 40), [
            (center_x, center_y - 10),
            (center_x - 3, center_y - 4),
            (center_x + 3, center_y - 4)
        ])
        pygame.draw.polygon(surface, (230, 40, 40), [
            (center_x - 3, center_y + 8),
            (center_x - 7, center_y + 12),
            (center_x - 3, center_y + 12)
        ])
        pygame.draw.polygon(surface, (230, 40, 40), [
            (center_x + 3, center_y + 8),
            (center_x + 7, center_y + 12),
            (center_x + 3, center_y + 12)
        ])

def draw_rocket_projectile(surface, rect):
    cx = rect.centerx
    # Body
    pygame.draw.rect(surface, WHITE, (rect.x + 2, rect.y + 6, 6, 14), border_radius=1)
    # Nose cone
    pygame.draw.polygon(surface, (230, 40, 40), [
        (cx, rect.y),
        (rect.x + 2, rect.y + 6),
        (rect.x + 8, rect.y + 6)
    ])
    # Fins
    pygame.draw.polygon(surface, (230, 40, 40), [
        (rect.x + 2, rect.y + 16),
        (rect.x - 2, rect.y + 22),
        (rect.x + 2, rect.y + 22)
    ])
    pygame.draw.polygon(surface, (230, 40, 40), [
        (rect.x + 8, rect.y + 16),
        (rect.x + 12, rect.y + 22),
        (rect.x + 8, rect.y + 22)
    ])
    # Flame tail particle
    if random.random() < 0.6:
        pygame.draw.rect(surface, GOLD, (cx - 2, rect.y + 20, 4, 6))

def draw_button_prompts(surface, x, y):
    # Space key cap
    space_rect = pygame.Rect(x, y, 75, 24)
    pygame.draw.rect(surface, (200, 200, 200), space_rect, border_radius=4)
    pygame.draw.rect(surface, (120, 120, 120), (x, y + 2, 75, 22), border_radius=4) # Shadow
    pygame.draw.rect(surface, WHITE, (x, y, 75, 22), border_radius=4) # Key top
    space_lbl = small_font.render("SPACE", True, BLACK)
    surface.blit(space_lbl, space_lbl.get_rect(center=(x + 37, y + 11)))
    
    # Or text
    or_lbl = small_font.render("or", True, WHITE)
    surface.blit(or_lbl, (x + 85, y + 4))
    
    # Controller X button
    pygame.draw.circle(surface, (45, 137, 239), (x + 120, y + 12), 12)
    pygame.draw.circle(surface, WHITE, (x + 120, y + 12), 12, 1)
    x_lbl = small_font.render("X", True, WHITE)
    surface.blit(x_lbl, x_lbl.get_rect(center=(x + 120, y + 11)))
    
    # Text instruction
    action_lbl = small_font.render("to launch Rocket!", True, WHITE)
    surface.blit(action_lbl, (x + 142, y + 4))


# Main game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Press R to restart
            if event.key == pygame.K_r and game_state != "playing":
                restart_game()

            # Press SPACE to launch rocket
            if event.key == pygame.K_SPACE and game_state == "playing" and rocket_ammo > 0:
                fire_rocket()

        # Handle gamepad hot-plugging
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joy.init()
            joysticks[joy.get_instance_id()] = joy
            print(f"Controller Connected: {joy.get_name()}")
            
        elif event.type == pygame.JOYDEVICEREMOVED:
            instance_id = event.instance_id
            if instance_id in joysticks:
                del joysticks[instance_id]
                print("Controller Disconnected")

        # Gamepad Button inputs
        if event.type == pygame.JOYBUTTONDOWN:
            if game_state == "playing":
                # Button 2 (X) to launch rocket
                if event.button == 2 and rocket_ammo > 0:
                    fire_rocket()
            else:
                # Button 0 (A/Cross) or Button 7 (Start) restarts
                if event.button in (0, 7):
                    restart_game()
            # Button 6 (Back/Select) to Quit
            if event.button == 6:
                running = False

    # Movement and collisions only happen while the game is being played
    if game_state == "playing":
        keys = pygame.key.get_pressed()

        # Update player speed dynamically depending on active booster
        if booster_active:
            player_speed = BOOSTED_PLAYER_SPEED
        else:
            player_speed = NORMAL_PLAYER_SPEED

        # Fetch Gamepad/Controller Analog & D-pad Axes inputs
        joy_dx = 0.0
        joy_dy = 0.0
        for joy in joysticks.values():
            # Read analog stick axes (axis 0 = X, axis 1 = Y)
            if joy.get_numaxes() >= 2:
                ax = joy.get_axis(0)
                ay = joy.get_axis(1)
                if abs(ax) > 0.2:  # Deadzone
                    joy_dx += ax
                if abs(ay) > 0.2:  # Deadzone
                    joy_dy += ay
                    
            # Read D-Pad (Hat) inputs
            if joy.get_numhats() > 0:
                hat = joy.get_hat(0)
                joy_dx += hat[0]
                joy_dy -= hat[1]  # Invert Hat Y to match screen coords

        # Combine Keyboard and Joystick Inputs (clamped to [-1, 1])
        dx = 0.0
        dy = 0.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1.0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1.0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1.0
            
        dx = max(-1.0, min(1.0, dx + joy_dx))
        dy = max(-1.0, min(1.0, dy + joy_dy))

        # Base scroll speed increases by 0.5 for every 100 points
        base_scroll_speed = 3.0 + (score // 100) * 0.5

        # Dynamic scroll speed based on player's vertical movement speed
        if dy < -0.1:     # Moving UP -> Scroll faster
            scroll_speed = base_scroll_speed * 1.6
        elif dy > 0.1:    # Moving DOWN -> Scroll slower
            scroll_speed = base_scroll_speed * 0.5
        else:
            scroll_speed = base_scroll_speed

        # Player horizontal movement constrained strictly to the roadway (200px to 600px)
        if dx > 0 and player_x < 600 - player_width:
            player_x += dx * player_speed
        elif dx < 0 and player_x > 200:
            player_x += dx * player_speed

        # Player vertical movement (capped below HUD boundary)
        if dy > 0 and player_y < HEIGHT - player_height:
            player_y += dy * player_speed
        elif dy < 0 and player_y > 95:
            player_y += dy * player_speed

        # Update the player's collision rectangle
        player_rect.x = player_x
        player_rect.y = player_y

        # Increment distance run (in meters)
        distance_run += scroll_speed * 0.05

        # Update active timers
        current_time = pygame.time.get_ticks()

        # Update player invulnerability flashing window
        if is_invulnerable:
            if current_time - invulnerable_timer > INVULNERABLE_DURATION:
                is_invulnerable = False

        if immunity_active:
            if current_time - immunity_timer > IMMUNITY_POWERUP_DURATION:
                immunity_active = False

        if booster_active:
            if current_time - booster_timer > BOOSTER_POWERUP_DURATION:
                booster_active = False

        # Emit booster flame tail particles
        if booster_active and random.random() < 0.4:
            particles.append({
                'x': player_x + player_width // 2 + random.randint(-5, 5),
                'y': player_y + player_height,
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(1, 3),
                'color': random.choice([GOLD, (255, 100, 0), (255, 50, 0)]),
                'radius': random.randint(4, 7),
                'life': 1.0
            })

        # Move obstacles and coins (vertical scrolling)
        for rock in obstacles:
            rock.y += scroll_speed
            if rock.y > HEIGHT:
                new_rock = spawn_safe_rock([r for r in obstacles if r != rock], coins)
                rock.x = new_rock.x
                rock.y = new_rock.y
                rock.width = new_rock.width
                rock.height = new_rock.height

        for c_rect in coins:
            c_rect.y += scroll_speed
            if c_rect.y > HEIGHT:
                new_coin = spawn_safe_coin(obstacles, [c for c in coins if c != c_rect])
                c_rect.x = new_coin.x
                c_rect.y = new_coin.y

        # Move active powerups
        for p in active_powerups[:]:
            p['rect'].y += scroll_speed
            if p['rect'].y > HEIGHT:
                active_powerups.remove(p)

        # Move active rockets
        for r in active_rockets[:]:
            r.y -= 12
            if r.y < 92:
                active_rockets.remove(r)
                continue
            
            # Rocket collision with rocks (obstacles)
            hit_obstacle = False
            for rock in obstacles:
                if r.colliderect(rock):
                    hit_obstacle = True
                    # Relocate rock
                    new_rock = spawn_safe_rock([other for other in obstacles if other != rock], coins)
                    rock.x = new_rock.x
                    rock.y = new_rock.y
                    rock.width = new_rock.width
                    rock.height = new_rock.height
                    
                    explosion_sound.play()
                    # Spawn particles
                    for _ in range(15):
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(2, 6)
                        particles.append({
                            'x': rock.centerx,
                            'y': rock.centery,
                            'vx': math.cos(angle) * speed,
                            'vy': math.sin(angle) * speed,
                            'color': random.choice([GOLD, (255, 100, 0), (255, 50, 0), WHITE]),
                            'radius': random.randint(3, 6),
                            'life': 1.0
                        })
                    break
            if hit_obstacle:
                active_rockets.remove(r)

        # Update particles physics
        for p in particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy'] + scroll_speed
            p['life'] -= 0.04
            if p['life'] <= 0:
                particles.remove(p)

        # Spawn periodic powerups
        if current_time - last_powerup_spawn > powerup_spawn_interval:
            if len(active_powerups) < 2:
                spawn_powerup()
            last_powerup_spawn = current_time

        # Scroll background decorations
        bg_offset = (bg_offset + scroll_speed) % HEIGHT
        for dec in decorations:
            dec['y'] += scroll_speed
            if dec['y'] > HEIGHT:
                dec['y'] = 92 - dec['size']
                side = random.choice(['left', 'right'])
                dec['x'] = random.randint(10, 170) if side == 'left' else random.randint(620, 770)
                dec['type'] = random.choice(['tree', 'grass', 'flower'])
                dec['color'] = random.choice([(18, 120, 58), (50, 160, 90), (220, 200, 50)])

        # Collision Check: Coin collections
        for c_rect in coins:
            if player_rect.colliderect(c_rect):
                score += 10
                coin_sound.play()
                
                # Relocate collected coin to a new random safe position above screen
                new_coin = spawn_safe_coin(obstacles, [c for c in coins if c != c_rect])
                c_rect.x = new_coin.x
                c_rect.y = new_coin.y

        # Collision Check: Powerup collections
        for p in active_powerups[:]:
            if player_rect.colliderect(p['rect']):
                p_type = p['type']
                active_powerups.remove(p)
                
                if p_type == 'immunity':
                    immunity_active = True
                    immunity_timer = current_time
                    powerup_sound.play()
                elif p_type == 'booster':
                    booster_active = True
                    booster_timer = current_time
                    powerup_sound.play()
                elif p_type == 'health':
                    lives = min(3, lives + 1)
                    heal_sound.play()
                elif p_type == 'rocket':
                    rocket_ammo += 1
                    powerup_sound.play()

        # Collision Check: Rock hits (ignored if invulnerable or immune)
        hit_rock = False
        if not is_invulnerable and not immunity_active:
            for rock in obstacles:
                if player_rect.colliderect(rock):
                    hit_rock = True
                    break
        
        if hit_rock:
            lives -= 1
            hit_sound.play()
            
            # Reset player positions
            player_x = 380
            player_y = 500
            player_rect.x = player_x
            player_rect.y = player_y
            
            # Start brief invulnerability
            is_invulnerable = True
            invulnerable_timer = pygame.time.get_ticks()
            
            # Reset obstacles/coins above the screen to avoid spawn trapping
            reset_obstacles_and_coins()

            # Health restore should be spawned when the player's life is 1
            if lives == 1:
                trigger_health_spawn()

            if lives <= 0:
                game_state = "lost"

    # DRAW GAME SCREEN
    # Fill background grass color (rich green)
    screen.fill((42, 120, 52))
    
    # Draw roadway (asphalt grey)
    pygame.draw.rect(screen, (95, 95, 100), (200, 92, 400, HEIGHT - 92))
    
    # Draw roadway edge borders (light grey lines)
    pygame.draw.rect(screen, (230, 230, 230), (196, 92, 4, HEIGHT - 92))
    pygame.draw.rect(screen, (230, 230, 230), (600, 92, 4, HEIGHT - 92))
    
    # Draw roadway dashed light grey center lanes (scrolling)
    line_height = 40
    gap = 40
    total_height = line_height + gap
    start_y = 92
    for y in range(start_y - total_height, HEIGHT, total_height):
        draw_y = y + (bg_offset % total_height)
        if draw_y < start_y:
            h_diff = start_y - draw_y
            if h_diff < line_height:
                pygame.draw.rect(screen, (230, 230, 230), (WIDTH // 2 - 4, start_y, 8, line_height - h_diff))
        elif draw_y + line_height > HEIGHT:
            h_diff = HEIGHT - draw_y
            if h_diff > 0:
                pygame.draw.rect(screen, (230, 230, 230), (WIDTH // 2 - 4, draw_y, 8, h_diff))
        else:
            pygame.draw.rect(screen, (230, 230, 230), (WIDTH // 2 - 4, draw_y, 8, line_height))

    # Draw scrolling background decorations (trees, flowers, grass tufts)
    for dec in decorations:
        if dec['type'] == 'tree':
            pygame.draw.rect(screen, (100, 60, 30), (dec['x'] - 2, dec['y'] + 2, 4, dec['size']))
            pygame.draw.circle(screen, dec['color'], (dec['x'], dec['y']), dec['size'])
        elif dec['type'] == 'grass':
            pygame.draw.line(screen, dec['color'], (dec['x'], dec['y']), (dec['x'] - 3, dec['y'] - dec['size']), 2)
            pygame.draw.line(screen, dec['color'], (dec['x'], dec['y']), (dec['x'], dec['y'] - dec['size'] - 2), 2)
            pygame.draw.line(screen, dec['color'], (dec['x'], dec['y']), (dec['x'] + 3, dec['y'] - dec['size']), 2)
        elif dec['type'] == 'flower':
            pygame.draw.line(screen, (50, 150, 50), (dec['x'], dec['y']), (dec['x'], dec['y'] + dec['size']), 2)
            pygame.draw.circle(screen, dec['color'], (dec['x'], dec['y']), 5)
            pygame.draw.circle(screen, WHITE, (dec['x'], dec['y']), 2)

    # Draw the rocks
    for rock in obstacles:
        pygame.draw.ellipse(screen, ROCK_GRAY, rock)
        pygame.draw.ellipse(
            screen,
            ROCK_LIGHT,
            (rock.x + 12, rock.y + 9, rock.width - 35, rock.height - 28),
        )
        pygame.draw.ellipse(screen, BLACK, rock, width=3)

    # Draw the STEM coins
    for c_rect in coins:
        screen.blit(coin_image, (c_rect.x, c_rect.y))

    # Draw active powerups
    for p in active_powerups:
        draw_collectible(screen, p['type'], p['rect'].x, p['rect'].y, p['rect'].width)

    # Draw active rockets
    for r in active_rockets:
        draw_rocket_projectile(screen, r)

    # Draw particles
    for p in particles:
        size = int(p['radius'] * p['life'])
        if size > 0:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), size)

    # Draw player character (flashing if currently invulnerable)
    draw_player = True
    if is_invulnerable:
        if (pygame.time.get_ticks() // 150) % 2 == 0:
            draw_player = False
            
    if draw_player:
        # Head
        pygame.draw.circle(screen, (112, 66, 42), (player_x + 20, player_y + 10), 10)
        # Shirt
        pygame.draw.rect(screen, BLUE, (player_x + 7, player_y + 19, 26, 24), border_radius=6)
        # Collar/V-neck
        pygame.draw.rect(screen, WHITE, (player_x + 13, player_y + 23, 14, 5), border_radius=2)
        # Legs
        pygame.draw.line(screen, BLACK, (player_x + 14, player_y + 42), (player_x + 10, player_y + 50), 4)
        pygame.draw.line(screen, BLACK, (player_x + 26, player_y + 42), (player_x + 30, player_y + 50), 4)

        # Draw player immunity shield glow
        if immunity_active:
            pulse = math.sin(pygame.time.get_ticks() * 0.015) * 3
            pygame.draw.circle(screen, LIGHT_BLUE, (player_x + player_width // 2, player_y + player_height // 2), 32 + int(pulse), 3)

    # Draw glassmorphic header panel (alpha-blitted floating container matching inspo.jpeg)
    # Margins: 10px from edges, 82px high (stretching from y=10 to y=92)
    header_surf = pygame.Surface((WIDTH - 20, 82), pygame.SRCALPHA)
    pygame.draw.rect(header_surf, (25, 25, 30, 200), (0, 0, WIDTH - 20, 82), border_radius=12)
    pygame.draw.rect(header_surf, (255, 255, 255, 55), (0, 0, WIDTH - 20, 82), width=2, border_radius=12)
    screen.blit(header_surf, (10, 10))

    # Draw logo emblem (as medallion on top-left, matching inspo.jpeg)
    screen.blit(coin_image, (25, 22))

    # Text headers (layout aligned matching inspo.jpeg)
    title_text = title_font.render("STEM TREASURE RUN", True, WHITE)
    score_text = hud_font.render(f"SCORE: {score}", True, WHITE)
    distance_text = hud_font.render(f"DISTANCE: {int(distance_run)}m", True, WHITE)
    screen.blit(title_text, (100, 18))
    screen.blit(score_text, (100, 52))
    screen.blit(distance_text, (550, 18))

    # Active power-ups remaining duration
    status_x = 300
    status_y = 54
    current_time = pygame.time.get_ticks()
    
    if immunity_active:
        rem = max(0.0, (IMMUNITY_POWERUP_DURATION - (current_time - immunity_timer)) / 1000.0)
        pygame.draw.circle(screen, LIGHT_BLUE, (status_x + 8, status_y + 10), 8)
        shield_text = small_font.render(f"SHIELD: {rem:.1f}s", True, LIGHT_BLUE)
        screen.blit(shield_text, (status_x + 22, status_y + 2))
        status_x += 120
        
    if booster_active:
        rem = max(0.0, (BOOSTER_POWERUP_DURATION - (current_time - booster_timer)) / 1000.0)
        pygame.draw.circle(screen, GOLD, (status_x + 8, status_y + 10), 8)
        boost_text = small_font.render(f"BOOST: {rem:.1f}s", True, GOLD)
        screen.blit(boost_text, (status_x + 22, status_y + 2))
        status_x += 110

    # Draw Lives using red heart icons next to text label (layout aligned matching inspo.jpeg)
    lives_label = hud_font.render("LIVES:", True, WHITE)
    screen.blit(lives_label, (550, 52))
    for i in range(3):
        heart_x = 635 + i * 28
        heart_y = 52
        if i < lives:
            draw_heart(screen, heart_x, heart_y, 20, (230, 40, 40))   # Filled Red Heart
        else:
            draw_heart(screen, heart_x, heart_y, 20, (60, 60, 60))    # Empty Container Lobe
            
    # Instructions at bottom of the screen (white text with drop shadow for readability over grass)
    instruction_str = "Arrow keys / WASD / Gamepad: Move    Collect coins to score!    Avoid the rocks!"
    shadow_text = small_font.render(instruction_str, True, (15, 15, 15))
    instruction_text = small_font.render(instruction_str, True, WHITE)
    screen.blit(shadow_text, (86, 571))
    screen.blit(instruction_text, (85, 570))

    # Rocket ready key display prompt overlay
    if game_state == "playing" and rocket_ammo > 0:
        overlay_rect = pygame.Rect(210, 98, 380, 36)
        pygame.draw.rect(screen, NAVY, overlay_rect, border_radius=8)
        pygame.draw.rect(screen, GOLD, overlay_rect, width=2, border_radius=8)
        draw_button_prompts(screen, 230, 104)

    # Win and game-over overlays
    # Game-over overlay
    if game_state == "lost":
        pygame.draw.rect(screen, NAVY, (125, 185, 550, 225), border_radius=22)
        pygame.draw.rect(screen, GOLD, (125, 185, 550, 225), width=4, border_radius=22)
        
        lose_text = message_font.render("GAME OVER", True, WHITE)
        score_display = hud_font.render(f"FINAL SCORE: {score}", True, GOLD)
        distance_display = hud_font.render(f"DISTANCE RUN: {int(distance_run)}m", True, WHITE)
        restart_text = hud_font.render("Press R / Gamepad A to try again or ESC to quit", True, WHITE)
        
        screen.blit(lose_text, lose_text.get_rect(center=(WIDTH // 2, 225)))
        screen.blit(score_display, score_display.get_rect(center=(WIDTH // 2, 275)))
        screen.blit(distance_display, distance_display.get_rect(center=(WIDTH // 2, 315)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, 365)))

    # Update display and control frame rate
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()

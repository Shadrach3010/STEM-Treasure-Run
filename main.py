import pygame
import random
import os
import math
import struct
import asyncio

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
    pothole_path = os.path.join(base_dir, "pothole.wav")
    combo_path = os.path.join(base_dir, "combo.wav")
    
    # Simple software synthesizer to generate 8-bit sound effects & music
    def generate_sound(filename, duration, type_sound):
        if os.path.exists(filename):
            return
        sample_rate = 22050
        num_samples = int(sample_rate * duration)
        
        # Standard WAV header (44 bytes for Mono, 16-bit PCM)
        data_size = num_samples * 2
        file_size = 36 + data_size
        header = struct.pack(
            '<4sI4s4sIHHIIHH4sI',
            b'RIFF',
            file_size,
            b'WAVE',
            b'fmt ',
            16,             # Subchunk1Size
            1,              # AudioFormat (1 = PCM)
            1,              # NumChannels (1 = Mono)
            sample_rate,    # SampleRate
            sample_rate * 2,# ByteRate
            2,              # BlockAlign
            16,             # BitsPerSample
            b'data',
            data_size
        )
        
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
            elif type_sound == 'pothole':
                # Low pitched squish
                freq = 120.0 - (t / duration) * 80.0
                import random as rnd
                noise = (rnd.random() * 2.0 - 1.0) * 0.15
                val = math.sin(2.0 * math.pi * freq * t) * 0.15 + noise
                decay = math.exp(-8.0 * t)
                val *= decay
            elif type_sound == 'combo':
                # Sparkling double arpeggio
                notes = [1046.50, 1318.51, 1567.98, 2093.00]
                note_idx = min(int(t / (duration / len(notes))), len(notes) - 1)
                freq = notes[note_idx]
                val = math.sin(2.0 * math.pi * freq * t) * 0.25
                decay = math.exp(-3.0 * t)
                val *= decay
            else:
                val = 0
            
            val = max(-1.0, min(1.0, val))
            sample = int(val * 32767)
            frames.extend(struct.pack('<h', sample))
        
        with open(filename, 'wb') as f:
            f.write(header)
            f.write(frames)

    generate_sound(music_path, 8.0, 'music')
    generate_sound(coin_path, 0.15, 'coin')
    generate_sound(hit_path, 0.3, 'hit')
    generate_sound(powerup_path, 0.32, 'powerup')
    generate_sound(rocket_launch_path, 0.3, 'rocket_launch')
    generate_sound(explosion_path, 0.5, 'explosion')
    generate_sound(heal_path, 0.3, 'heal')
    generate_sound(pothole_path, 0.25, 'pothole')
    generate_sound(combo_path, 0.2, 'combo')

# Initialize Pygame and audio mixer
pygame.init()
pygame.mixer.init()

# Game settings
WIDTH = 1000
HEIGHT = 600
FPS = 60

# Dynamic road settings
ROAD_WIDTH = 460
ROAD_LEFT = (WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH

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

# Create the game window with double buffering for smooth rendering
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("STEM Treasure Run")

# Optimize rendering surfaces by instantiating them once to prevent garbage collection frame-drops
light_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
darkness_surf = pygame.Surface((WIDTH, HEIGHT - 92), pygame.SRCALPHA)
header_surf = pygame.Surface((WIDTH - 20, 82), pygame.SRCALPHA)
# Pre-draw static glassmorphic header background and borders to save redraw calls
pygame.draw.rect(header_surf, (25, 25, 30, 200), (0, 0, WIDTH - 20, 82), border_radius=12)
pygame.draw.rect(header_surf, (255, 255, 255, 55), (0, 0, WIDTH - 20, 82), width=2, border_radius=12)

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
pothole_sound = pygame.mixer.Sound("assets/pothole.wav")
pothole_sound.set_volume(0.5)
combo_sound = pygame.mixer.Sound("assets/combo.wav")
combo_sound.set_volume(0.5)

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
player_vx = 0.0
player_vy = 0.0
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
NORMAL_PLAYER_SPEED = 7
BOOSTED_PLAYER_SPEED = 12

rocket_ammo = 0
distance_run = 0.0

# Side Buildings
active_buildings = []
last_building_spawn = 0
building_spawn_interval = 3500 # 3.5 seconds

# Day/Night Cycle
time_of_day = 0.0 # Cycles smoothly

# Combo System
combo_multiplier = 1
combo_timer = 0
COMBO_MAX_TIME = 150 # 2.5 seconds at 60 FPS

# Slow status (Pothole hit)
is_slowed = False
slowed_timer = 0
SLOWED_DURATION = 2000 # 2 seconds

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
    x = random.randint(10, ROAD_LEFT - 30) if side == 'left' else random.randint(ROAD_RIGHT + 20, WIDTH - 30)
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

def spawn_safe_obstacle(other_obstacles, other_coins, obstacle_type=None):
    if not obstacle_type:
        obstacle_type = random.choices(['rock', 'log', 'pothole'], weights=[60, 20, 20])[0]
        
    while True:
        y = random.randint(-250, -50)
        if obstacle_type == 'rock':
            w = random.randint(70, 85)
            h = random.randint(50, 65)
            x = random.randint(ROAD_LEFT - 40, ROAD_RIGHT - w + 40)
        elif obstacle_type == 'log':
            w = random.randint(90, 110)
            h = random.randint(30, 40)
            x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - w - 10)
        elif obstacle_type == 'pothole':
            w = random.randint(60, 75)
            h = random.randint(40, 50)
            x = random.randint(ROAD_LEFT + 15, ROAD_RIGHT - w - 15)
            
        rect = pygame.Rect(x, y, w, h)
        
        # Ensure no overlap with other obstacles or coins
        overlap = False
        for other in other_obstacles:
            if rect.colliderect(other['rect']):
                overlap = True
                break
        for coin in other_coins:
            if rect.colliderect(coin):
                overlap = True
                break
        if not overlap:
            return {'rect': rect, 'type': obstacle_type}

def spawn_safe_coin(other_rocks, other_coins):
    while True:
        # Coins spawn mostly on the central roadway
        x = random.randint(ROAD_LEFT + 15, ROAD_RIGHT - 15 - 58)
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
    
    # Spawn initial obstacles
    for i in range(3):
        obs = spawn_safe_obstacle(obstacles, coins, 'rock')
        obs['rect'].y = -100 - i * 180
        obstacles.append(obs)
        
    for i in range(2):
        coin = spawn_safe_coin([o['rect'] for o in obstacles], coins)
        coin.y = -200 - i * 250
        coins.append(coin)

def restart_game():
    global score, lives, game_state, player_x, player_y, player_vx, player_vy, is_invulnerable, bg_offset
    global active_powerups, active_rockets, particles
    global immunity_active, immunity_timer, booster_active, booster_timer, rocket_ammo
    global last_powerup_spawn, distance_run
    global active_buildings, last_building_spawn, time_of_day
    global combo_multiplier, combo_timer, is_slowed, slowed_timer
    score = 0
    lives = 3
    game_state = "playing"
    player_x = 380
    player_y = 500
    player_vx = 0.0
    player_vy = 0.0
    player_rect.x = player_x
    player_rect.y = player_y
    is_invulnerable = False
    bg_offset = 0.0
    
    # Reset lists
    active_powerups = []
    active_rockets = []
    particles = []
    active_buildings = []
    
    # Reset powerup variables
    immunity_active = False
    immunity_timer = 0
    booster_active = False
    booster_timer = 0
    rocket_ammo = 0
    distance_run = 0.0
    last_powerup_spawn = pygame.time.get_ticks()
    last_building_spawn = pygame.time.get_ticks()
    
    # Reset cycle, combo and slow states
    time_of_day = 0.0
    combo_multiplier = 1
    combo_timer = 0
    is_slowed = False
    slowed_timer = 0

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
        # Powerups spawn on roadway
        x = random.randint(ROAD_LEFT + 15, ROAD_RIGHT - 15 - 40)
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
            
    rect = spawn_safe_powerup([o['rect'] for o in obstacles], coins, active_powerups)
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

def spawn_building(side=None):
    global active_buildings
    if not side:
        side = random.choice(['left', 'right'])
    
    btype = random.choices(['house', 'church', 'school'], weights=[60, 20, 20])[0]
    
    if btype == 'house':
        w = random.randint(55, 70)
        h = random.randint(50, 65)
        color = random.choice([(180, 80, 50), (60, 120, 180), (200, 160, 40), (80, 150, 90)])
    elif btype == 'church':
        w = random.randint(60, 70)
        h = random.randint(85, 105)
        color = (220, 220, 225) # Light grey stone church
    elif btype == 'school':
        w = random.randint(85, 105)
        h = random.randint(65, 80)
        color = (160, 50, 50) # Brick red
        
    # Try to find a non-overlapping position
    for _ in range(50):
        if side == 'left':
            x = random.randint(15, ROAD_LEFT - 15 - w)
        else:
            x = random.randint(ROAD_RIGHT + 15, WIDTH - 15 - w)
        y = random.randint(-220, -120)
        rect = pygame.Rect(x, y, w, h)
        
        overlap = False
        for b in active_buildings:
            if rect.colliderect(b['rect']):
                overlap = True
                break
        if not overlap:
            active_buildings.append({
                'rect': rect,
                'type': btype,
                'side': side,
                'color': color
            })
            break

def draw_building(surface, b):
    rect = b['rect']
    btype = b['type']
    color = b['color']
    
    # Walls shadow
    pygame.draw.rect(surface, (20, 20, 20), (rect.x + 2, rect.y + 2, rect.width, rect.height), border_radius=4)
    # Walls
    pygame.draw.rect(surface, color, rect, border_radius=4)
    pygame.draw.rect(surface, BLACK, rect, width=2, border_radius=4)
    
    # Draw features based on type
    if btype == 'house':
        # Roof (triangular)
        roof_pts = [
            (rect.x - 4, rect.y + 5),
            (rect.centerx, rect.y - 20),
            (rect.right + 4, rect.y + 5)
        ]
        # Shadow under roof
        pygame.draw.polygon(surface, (100, 30, 20), roof_pts)
        pygame.draw.polygon(surface, BLACK, roof_pts, 2)
        
        # Door
        door_w = 14
        door_h = 24
        pygame.draw.rect(surface, (90, 50, 30), (rect.centerx - door_w//2, rect.bottom - door_h - 2, door_w, door_h))
        pygame.draw.rect(surface, BLACK, (rect.centerx - door_w//2, rect.bottom - door_h - 2, door_w, door_h), 1)
        
        # Window
        pygame.draw.rect(surface, GOLD, (rect.x + 8, rect.y + 12, 12, 12))
        pygame.draw.rect(surface, BLACK, (rect.x + 8, rect.y + 12, 12, 12), 1)
        pygame.draw.rect(surface, GOLD, (rect.right - 20, rect.y + 12, 12, 12))
        pygame.draw.rect(surface, BLACK, (rect.right - 20, rect.y + 12, 12, 12), 1)
        
    elif btype == 'church':
        # Steeple spire on top
        spire_w = 20
        spire_h = 35
        spire_rect = pygame.Rect(rect.centerx - spire_w//2, rect.y - spire_h, spire_w, spire_h)
        pygame.draw.rect(surface, color, spire_rect)
        pygame.draw.rect(surface, BLACK, spire_rect, 2)
        
        # Cross on top of spire
        cross_x = rect.centerx
        cross_y = rect.y - spire_h - 10
        pygame.draw.line(surface, GOLD, (cross_x, cross_y - 8), (cross_x, cross_y + 12), 3)
        pygame.draw.line(surface, GOLD, (cross_x - 8, cross_y), (cross_x + 8, cross_y), 3)
        
        # Double doors
        door_w = 22
        door_h = 32
        pygame.draw.rect(surface, (60, 30, 20), (rect.centerx - door_w//2, rect.bottom - door_h - 2, door_w, door_h), border_radius=2)
        pygame.draw.rect(surface, BLACK, (rect.centerx - door_w//2, rect.bottom - door_h - 2, door_w, door_h), 2, border_radius=2)
        pygame.draw.line(surface, BLACK, (rect.centerx, rect.bottom - door_h - 2), (rect.centerx, rect.bottom - 2), 1)
        
        # Stained glass window (glowing blue/yellow arched window)
        win_rect = pygame.Rect(rect.centerx - 8, rect.y + 12, 16, 24)
        pygame.draw.rect(surface, (95, 188, 235), win_rect, border_radius=4)
        pygame.draw.rect(surface, BLACK, win_rect, 1, border_radius=4)
        pygame.draw.line(surface, BLACK, (rect.centerx, rect.y + 12), (rect.centerx, rect.y + 36), 1)
        
    elif btype == 'school':
        # Bell tower on roof
        tower_pts = [
            (rect.centerx - 12, rect.y),
            (rect.centerx - 12, rect.y - 15),
            (rect.centerx + 12, rect.y - 15),
            (rect.centerx + 12, rect.y)
        ]
        pygame.draw.polygon(surface, color, tower_pts)
        pygame.draw.polygon(surface, BLACK, tower_pts, 2)
        # Bell
        pygame.draw.circle(surface, GOLD, (rect.centerx, rect.y - 6), 5)
        
        # Double doors
        door_w = 20
        door_h = 28
        pygame.draw.rect(surface, (80, 80, 80), (rect.centerx - door_w//2, rect.bottom - door_h - 2, door_w, door_h))
        pygame.draw.rect(surface, BLACK, (rect.centerx - door_w//2, rect.bottom - door_h - 2, door_w, door_h), 2)
        
        # Windows row
        for offset in [10, 30, rect.width - 22, rect.width - 42]:
            win_x = rect.x + offset
            pygame.draw.rect(surface, GOLD, (win_x, rect.y + 10, 12, 18))
            pygame.draw.rect(surface, BLACK, (win_x, rect.y + 10, 12, 18), 1)


async def main():
    global running, player_x, player_y, game_state, score, lives, is_invulnerable, invulnerable_timer
    global active_powerups, active_rockets, particles, active_buildings, last_building_spawn, time_of_day
    global combo_multiplier, combo_timer, is_slowed, slowed_timer, last_powerup_spawn, distance_run, scroll_speed, bg_offset, rocket_ammo, player_speed
    global booster_active, booster_timer, immunity_active, immunity_timer
    global player_vx, player_vy

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
    
            # Update player speed dynamically depending on active booster and slow status
            if is_slowed:
                player_speed = 2
            elif booster_active:
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
                
            # Calculate target input direction
            target_dx = max(-1.0, min(1.0, dx + joy_dx))
            target_dy = max(-1.0, min(1.0, dy + joy_dy))
            
            # Accelerate player velocity towards target inputs (yielding smooth keyboard and gamepad ramps)
            accel = 0.95
            friction = 0.84
            
            if abs(target_dx) > 0.01:
                player_vx += target_dx * accel
            else:
                player_vx *= friction
                
            if abs(target_dy) > 0.01:
                player_vy += target_dy * accel
            else:
                player_vy *= friction
                
            # Clamp player velocities to current max speed limits
            player_vx = max(-player_speed, min(player_speed, player_vx))
            player_vy = max(-player_speed, min(player_speed, player_vy))
    
            # Base scroll speed starts faster (4.5) and increases with score
            base_scroll_speed = 4.5 + (score // 100) * 0.6
    
            # Dynamic scroll speed based on player's actual vertical velocity
            norm_vy = player_vy / player_speed if player_speed > 0 else 0
            if norm_vy < -0.1:     # Moving UP -> Scroll faster
                scroll_speed = base_scroll_speed * 1.6
            elif norm_vy > 0.1:    # Moving DOWN -> Scroll slower
                scroll_speed = base_scroll_speed * 0.5
            else:
                scroll_speed = base_scroll_speed
    
            # Apply velocities to player positions
            player_x += player_vx
            player_y += player_vy
            
            # Constrain player strictly to the roadway and zero out velocity upon border contact
            if player_x < ROAD_LEFT:
                player_x = ROAD_LEFT
                player_vx = 0.0
            elif player_x > ROAD_RIGHT - player_width:
                player_x = ROAD_RIGHT - player_width
                player_vx = 0.0
                
            if player_y < 95:
                player_y = 95
                player_vy = 0.0
            elif player_y > HEIGHT - player_height:
                player_y = HEIGHT - player_height
                player_vy = 0.0
    
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
    
            # Move obstacles (vertical scrolling)
            for obs in obstacles:
                obs['rect'].y += scroll_speed
                if obs['rect'].y > HEIGHT:
                    new_obs = spawn_safe_obstacle([o for o in obstacles if o != obs], coins)
                    obs['rect'].x = new_obs['rect'].x
                    obs['rect'].y = new_obs['rect'].y
                    obs['rect'].width = new_obs['rect'].width
                    obs['rect'].height = new_obs['rect'].height
                    obs['type'] = new_obs['type']
    
            # Move coins (vertical scrolling)
            for c_rect in coins:
                c_rect.y += scroll_speed
                if c_rect.y > HEIGHT:
                    new_coin = spawn_safe_coin([o['rect'] for o in obstacles], [c for c in coins if c != c_rect])
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
                
                # Rocket collision with obstacles
                hit_obstacle = False
                for obs in obstacles:
                    if r.colliderect(obs['rect']):
                        hit_obstacle = True
                        # Relocate obstacle
                        new_obs = spawn_safe_obstacle([other for other in obstacles if other != obs], coins)
                        obs['rect'].x = new_obs['rect'].x
                        obs['rect'].y = new_obs['rect'].y
                        obs['rect'].width = new_obs['rect'].width
                        obs['rect'].height = new_obs['rect'].height
                        obs['type'] = new_obs['type']
                        
                        explosion_sound.play()
                        # Spawn explosion particles
                        for _ in range(15):
                            angle = random.uniform(0, 2 * math.pi)
                            speed = random.uniform(2, 6)
                            particles.append({
                                'x': obs['rect'].centerx,
                                'y': obs['rect'].centery,
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
    
            # Move active buildings
            for b in active_buildings[:]:
                b['rect'].y += scroll_speed
                if b['rect'].y > HEIGHT:
                    active_buildings.remove(b)
    
            # Spawn buildings periodically
            if current_time - last_building_spawn > building_spawn_interval:
                if len(active_buildings) < 8:
                    spawn_building()
                last_building_spawn = current_time
    
            # Update time of day (day/night cycle)
            time_of_day = (time_of_day + 0.002) % (2 * math.pi)
    
            # Decay combo timer
            if combo_timer > 0:
                combo_timer -= 1
            else:
                combo_multiplier = 1
    
            # Update slow status (pothole slowdown decay)
            if is_slowed:
                if current_time - slowed_timer > SLOWED_DURATION:
                    is_slowed = False
    
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
                    dec['x'] = random.randint(10, ROAD_LEFT - 30) if side == 'left' else random.randint(ROAD_RIGHT + 20, WIDTH - 30)
                    dec['type'] = random.choice(['tree', 'grass', 'flower'])
                    dec['color'] = random.choice([(18, 120, 58), (50, 160, 90), (220, 200, 50)])
    
            # Collision Check: Coin collections
            for c_rect in coins:
                if player_rect.colliderect(c_rect):
                    combo_sound.play()
                    
                    # Apply combo multiplier to score
                    score += 10 * combo_multiplier
                    
                    # Build combo multiplier
                    combo_multiplier = min(5, combo_multiplier + 1)
                    combo_timer = COMBO_MAX_TIME
                    
                    # Spawn coin sparkle particles
                    for _ in range(12):
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(1.5, 4)
                        particles.append({
                            'x': c_rect.centerx,
                            'y': c_rect.centery,
                            'vx': math.cos(angle) * speed,
                            'vy': math.sin(angle) * speed,
                            'color': GOLD,
                            'radius': random.randint(2, 5),
                            'life': 1.0
                        })
                    
                    # Relocate collected coin to a new random safe position above screen
                    new_coin = spawn_safe_coin([o['rect'] for o in obstacles], [c for c in coins if c != c_rect])
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
    
            # Collision Check: Obstacle hits (ignored if invulnerable or immune)
            hit_obstacle = False
            if not is_invulnerable and not immunity_active:
                for obs in obstacles:
                    if player_rect.colliderect(obs['rect']):
                        if obs['type'] == 'pothole':
                            # Slow player and trigger mud sound
                            is_slowed = True
                            slowed_timer = current_time
                            pothole_sound.play()
                            
                            # Relocate pothole
                            new_obs = spawn_safe_obstacle([other for other in obstacles if other != obs], coins)
                            obs['rect'].x = new_obs['rect'].x
                            obs['rect'].y = new_obs['rect'].y
                            obs['rect'].width = new_obs['rect'].width
                            obs['rect'].height = new_obs['rect'].height
                            obs['type'] = new_obs['type']
                        else:
                            hit_obstacle = True
                            break
            
            if hit_obstacle:
                lives -= 1
                hit_sound.play()
                
                # Reset player positions
                player_x = 380
                player_y = 500
                player_rect.x = player_x
                player_rect.y = player_y
                
                # Reset combos on hit
                combo_multiplier = 1
                combo_timer = 0
                is_slowed = False
                
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
        pygame.draw.rect(screen, (95, 95, 100), (ROAD_LEFT, 92, ROAD_WIDTH, HEIGHT - 92))
        
        # Draw roadway edge borders (light grey lines)
        pygame.draw.rect(screen, (230, 230, 230), (ROAD_LEFT - 4, 92, 4, HEIGHT - 92))
        pygame.draw.rect(screen, (230, 230, 230), (ROAD_RIGHT, 92, 4, HEIGHT - 92))
        
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
    
        # Draw side buildings
        for b in active_buildings:
            draw_building(screen, b)
    
        # Draw the obstacles (rocks, logs, potholes)
        for obs in obstacles:
            rect = obs['rect']
            otype = obs['type']
            if otype == 'rock':
                pygame.draw.ellipse(screen, ROCK_GRAY, rect)
                pygame.draw.ellipse(
                    screen,
                    ROCK_LIGHT,
                    (rect.x + 12, rect.y + 9, rect.width - 35, rect.height - 28),
                )
                pygame.draw.ellipse(screen, BLACK, rect, width=3)
            elif otype == 'log':
                # Wood texture rectangle
                pygame.draw.rect(screen, (100, 60, 30), rect, border_radius=4)
                pygame.draw.rect(screen, (80, 45, 20), rect, width=2, border_radius=4)
                # Log inner details
                pygame.draw.line(screen, (80, 45, 20), (rect.x + 10, rect.y + 10), (rect.x + rect.width - 10, rect.y + 10), 2)
                pygame.draw.line(screen, (80, 45, 20), (rect.x + 15, rect.y + rect.height - 10), (rect.x + rect.width - 15, rect.y + rect.height - 10), 2)
            elif otype == 'pothole':
                # Dark mud puddle/hole on road
                pygame.draw.ellipse(screen, (40, 40, 40), rect)
                pygame.draw.ellipse(screen, BLACK, rect, width=2)
                pygame.draw.line(screen, BLACK, (rect.x, rect.centery), (rect.x - 6, rect.centery), 2)
                pygame.draw.line(screen, BLACK, (rect.right, rect.centery), (rect.right + 6, rect.centery), 2)
    
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
    
        # Draw player headlight cone projection at dusk/night
        ambient_alpha = int(max(0, math.sin(time_of_day) * 160))
        if ambient_alpha > 30:
            # Clear and reuse pre-allocated light surface
            light_surf.fill((0, 0, 0, 0))
            pts = [
                (player_x + player_width // 2 - 5, player_y + 10),
                (player_x + player_width // 2 + 5, player_y + 10),
                (player_x + player_width // 2 + 100, player_y - 200),
                (player_x + player_width // 2 - 100, player_y - 200)
            ]
            # Translucent yellow light cone
            light_alpha = min(150, int(ambient_alpha * 0.9))
            pygame.draw.polygon(light_surf, (255, 255, 200, light_alpha), pts)
            # Add soft circle highlight at end of beam
            pygame.draw.ellipse(light_surf, (255, 255, 220, int(light_alpha * 0.4)), (player_x + player_width // 2 - 100, player_y - 220, 200, 40))
            screen.blit(light_surf, (0, 0))
    
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
    
            # Draw player mud/slow indicator
            if is_slowed:
                mud_lbl = small_font.render("SLOW!", True, (150, 75, 0))
                screen.blit(mud_lbl, (player_x + player_width + 5, player_y + 25))
    
            # Draw combo popup next to the player's head
            if combo_multiplier > 1:
                combo_lbl = small_font.render(f"x{combo_multiplier} Combo!", True, GOLD)
                screen.blit(combo_lbl, (player_x + player_width + 5, player_y - 5))
    
        # Draw ambient darkness overlay for Day/Night cycle below the HUD
        if ambient_alpha > 0:
            # Clear and reuse pre-allocated darkness surface
            darkness_surf.fill((0, 0, 0, 0))
            darkness_surf.fill((10, 10, 28, ambient_alpha)) # Dark blue/night tint
            # Cutouts for house windows to glow!
            for b in active_buildings:
                brect = b['rect']
                if brect.y + brect.height > 92 and brect.y < HEIGHT:
                    rel_y = brect.y - 92
                    if b['type'] == 'house':
                        pygame.draw.rect(darkness_surf, (0, 0, 0, 0), (brect.x + 8, rel_y + 12, 12, 12))
                        pygame.draw.rect(darkness_surf, (0, 0, 0, 0), (brect.right - 20, rel_y + 12, 12, 12))
                    elif b['type'] == 'church':
                        pygame.draw.rect(darkness_surf, (0, 0, 0, 0), (brect.centerx - 8, rel_y + 12, 16, 24))
                    elif b['type'] == 'school':
                        for offset in [10, 30, brect.width - 22, brect.width - 42]:
                            pygame.draw.rect(darkness_surf, (0, 0, 0, 0), (brect.x + offset, rel_y + 10, 12, 18))
            screen.blit(darkness_surf, (0, 92))
    
        # Draw glassmorphic header panel (using pre-allocated static header surface)
        screen.blit(header_surf, (10, 10))
    
        # Draw logo emblem (as medallion on top-left, matching inspo.jpeg)
        screen.blit(coin_image, (25, 22))
    
        # Text headers (layout aligned matching inspo.jpeg)
        title_text = title_font.render("STEM TREASURE RUN", True, WHITE)
        if combo_multiplier > 1:
            score_text = hud_font.render(f"SCORE: {score} ({combo_multiplier}x Combo!)", True, GOLD)
        else:
            score_text = hud_font.render(f"SCORE: {score}", True, WHITE)
        distance_text = hud_font.render(f"DISTANCE: {int(distance_run)}m", True, WHITE)
        screen.blit(title_text, (100, 18))
        screen.blit(score_text, (100, 52))
        screen.blit(distance_text, (WIDTH - 250, 18))
    
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
        screen.blit(lives_label, (WIDTH - 250, 52))
        for i in range(3):
            heart_x = WIDTH - 165 + i * 28
            heart_y = 52
            if i < lives:
                draw_heart(screen, heart_x, heart_y, 20, (230, 40, 40))   # Filled Red Heart
            else:
                draw_heart(screen, heart_x, heart_y, 20, (60, 60, 60))    # Empty Container Lobe
                
        # Instructions at bottom of the screen (white text with drop shadow for readability over grass)
        instruction_str = "Arrow keys / WASD / Gamepad: Move    Collect coins to score!    Avoid the rocks!"
        shadow_text = small_font.render(instruction_str, True, (15, 15, 15))
        instruction_text = small_font.render(instruction_str, True, WHITE)
        screen.blit(shadow_text, shadow_text.get_rect(center=(WIDTH // 2, 576)))
        screen.blit(instruction_text, instruction_text.get_rect(center=(WIDTH // 2, 575)))
    
        # Rocket ready key display prompt overlay
        if game_state == "playing" and rocket_ammo > 0:
            overlay_rect = pygame.Rect(ROAD_LEFT + 10, 98, ROAD_WIDTH - 20, 36)
            pygame.draw.rect(screen, NAVY, overlay_rect, border_radius=8)
            pygame.draw.rect(screen, GOLD, overlay_rect, width=2, border_radius=8)
            draw_button_prompts(screen, ROAD_LEFT + 30, 104)
    
        # Win and game-over overlays
        # Game-over overlay
        if game_state == "lost":
            over_w = 550
            over_x = (WIDTH - over_w) // 2
            pygame.draw.rect(screen, NAVY, (over_x, 185, over_w, 225), border_radius=22)
            pygame.draw.rect(screen, GOLD, (over_x, 185, over_w, 225), width=4, border_radius=22)
            
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
        await asyncio.sleep(0)
    
    # Quit Pygame
    pygame.quit()

asyncio.run(main())

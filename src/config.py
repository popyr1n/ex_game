"""Game configuration and level presets for Perque promo platformer."""

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
GRAVITY = 0.7
PLAYER_SPEED = 5
JUMP_SPEED = -14
PLAYER_MAX_HP = 5

BRAND_NAME = "PERQUE"
PROMO_CODE = "PERQUE-HERO-15"

WEAPONS = {
    "basic": {"damage": 1, "cooldown": 360, "bullet_speed": 8, "color": (255, 255, 255)},
    "burst": {"damage": 1, "cooldown": 190, "bullet_speed": 10, "color": (255, 200, 80)},
    "plasma": {"damage": 2, "cooldown": 420, "bullet_speed": 12, "color": (120, 220, 255)},
}

LEVELS = [
    {
        "name": "Уровень 1: Невский Разгон",
        "player_spawn": (80, 380),
        "platforms": [
            (0, 500, 960, 40),
            (180, 430, 160, 20),
            (400, 360, 180, 20),
            (660, 300, 200, 20),
        ],
        "enemies": [
            {"x": 270, "y": 398, "w": 34, "h": 34, "hp": 2, "speed": 1.4},
            {"x": 740, "y": 268, "w": 34, "h": 34, "hp": 2, "speed": 1.6},
        ],
        "weapon_pickups": [
            {"x": 450, "y": 322, "weapon": "burst"},
        ],
        "exit": (890, 250, 40, 80),
    },
    {
        "name": "Уровень 2: Крыши Питера",
        "player_spawn": (60, 380),
        "platforms": [
            (0, 500, 960, 40),
            (130, 430, 120, 20),
            (320, 370, 120, 20),
            (510, 320, 130, 20),
            (700, 260, 150, 20),
            (350, 250, 110, 20),
        ],
        "enemies": [
            {"x": 150, "y": 398, "w": 34, "h": 34, "hp": 2, "speed": 1.8},
            {"x": 530, "y": 288, "w": 34, "h": 34, "hp": 3, "speed": 2.2},
            {"x": 740, "y": 228, "w": 34, "h": 34, "hp": 3, "speed": 2.0},
        ],
        "weapon_pickups": [
            {"x": 370, "y": 212, "weapon": "plasma"},
        ],
        "exit": (900, 200, 40, 80),
    },
    {
        "name": "Уровень 3: Финальный Подиум",
        "player_spawn": (60, 380),
        "platforms": [
            (0, 500, 960, 40),
            (150, 410, 130, 20),
            (320, 360, 120, 20),
            (500, 300, 140, 20),
            (710, 260, 190, 20),
        ],
        "enemies": [
            {"x": 200, "y": 378, "w": 34, "h": 34, "hp": 3, "speed": 2.2},
            {"x": 540, "y": 268, "w": 34, "h": 34, "hp": 3, "speed": 2.4},
        ],
        "weapon_pickups": [],
        "boss": {"x": 760, "y": 188, "w": 90, "h": 90, "hp": 14, "speed": 2.0},
    },
]

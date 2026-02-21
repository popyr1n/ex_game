"""Level loading utilities."""

from __future__ import annotations

import pygame

from .config import LEVELS
from .entities import Boss, Enemy, ExitPortal, WeaponPickup


class LevelState:
    def __init__(self, index: int):
        raw = LEVELS[index]
        self.name = raw["name"]
        self.platforms = [pygame.Rect(*p) for p in raw["platforms"]]
        self.enemies = [Enemy(**e) for e in raw.get("enemies", [])]
        self.pickups = [WeaponPickup(**pickup) for pickup in raw.get("weapon_pickups", [])]
        self.exit = ExitPortal(raw["exit"]) if "exit" in raw else None
        self.boss = Boss(**raw["boss"]) if "boss" in raw else None
        self.player_spawn = raw["player_spawn"]

    @property
    def complete(self):
        enemies_cleared = all(not enemy.alive for enemy in self.enemies)
        if self.boss:
            return enemies_cleared and not self.boss.alive
        return enemies_cleared

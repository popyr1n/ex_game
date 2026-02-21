"""Game entities for platformer prototype."""

from __future__ import annotations

import pygame

from .config import (
    GRAVITY,
    JUMP_SPEED,
    PLAYER_MAX_HP,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WEAPONS,
)


class Player:
    def __init__(self, pos: tuple[int, int]):
        self.rect = pygame.Rect(pos[0], pos[1], 34, 48)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.facing = 1
        self.hp = PLAYER_MAX_HP
        self.weapon = "basic"
        self.last_shot_ms = 0

    def handle_input(self, keys: pygame.key.ScancodeWrapper):
        self.velocity.x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity.x = -PLAYER_SPEED
            self.facing = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity.x = PLAYER_SPEED
            self.facing = 1

    def jump(self):
        if self.on_ground:
            self.velocity.y = JUMP_SPEED
            self.on_ground = False

    def update(self, platforms: list[pygame.Rect]):
        self.velocity.y += GRAVITY
        if self.velocity.y > 13:
            self.velocity.y = 13

        self.rect.x += int(self.velocity.x)
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity.x > 0:
                    self.rect.right = platform.left
                elif self.velocity.x < 0:
                    self.rect.left = platform.right

        self.rect.y += int(self.velocity.y)
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity.y > 0:
                    self.rect.bottom = platform.top
                    self.velocity.y = 0
                    self.on_ground = True
                elif self.velocity.y < 0:
                    self.rect.top = platform.bottom
                    self.velocity.y = 0

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top > SCREEN_HEIGHT:
            self.hp = 0

    def can_shoot(self, now_ms: int) -> bool:
        return now_ms - self.last_shot_ms >= WEAPONS[self.weapon]["cooldown"]

    def shoot(self, now_ms: int):
        self.last_shot_ms = now_ms
        data = WEAPONS[self.weapon]
        return Bullet(
            x=self.rect.centerx,
            y=self.rect.centery,
            direction=self.facing,
            speed=data["bullet_speed"],
            damage=data["damage"],
            color=data["color"],
        )


class Bullet:
    def __init__(self, x: int, y: int, direction: int, speed: int, damage: int, color: tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, 14, 6)
        self.speed = speed * direction
        self.damage = damage
        self.color = color

    def update(self):
        self.rect.x += self.speed

    @property
    def alive(self):
        return -30 <= self.rect.x <= SCREEN_WIDTH + 30


class Enemy:
    def __init__(self, x: int, y: int, w: int, h: int, hp: int, speed: float):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.hp = hp
        self.base_x = x
        self.direction = 1
        self.patrol_distance = 80
        self.damage_cooldown = 0

    def update(self):
        self.rect.x += int(self.speed * self.direction)
        if self.rect.x < self.base_x - self.patrol_distance:
            self.direction = 1
        elif self.rect.x > self.base_x + self.patrol_distance:
            self.direction = -1

    def apply_damage(self, amount: int):
        self.hp -= amount

    @property
    def alive(self):
        return self.hp > 0


class Boss(Enemy):
    def __init__(self, x: int, y: int, w: int, h: int, hp: int, speed: float):
        super().__init__(x, y, w, h, hp, speed)
        self.patrol_distance = 120


class WeaponPickup:
    def __init__(self, x: int, y: int, weapon: str):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.weapon = weapon
        self.active = True


class ExitPortal:
    def __init__(self, rect_data: tuple[int, int, int, int]):
        self.rect = pygame.Rect(*rect_data)

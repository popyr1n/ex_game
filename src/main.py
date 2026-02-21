"""Perque arcade platformer prototype using pygame."""

from __future__ import annotations

import pygame

from .config import BRAND_NAME, FPS, LEVELS, PROMO_CODE, SCREEN_HEIGHT, SCREEN_WIDTH
from .entities import Player
from .levels import LevelState


def draw_text(screen, text, size, color, x, y, center=False):
    font = pygame.font.SysFont("arial", size, bold=True)
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)


def run():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"{BRAND_NAME} Fan Service: Street Runner")
    clock = pygame.time.Clock()

    level_index = 0
    level = LevelState(level_index)
    player = Player(level.player_spawn)
    bullets = []
    state = "menu"

    while True:
        dt = clock.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if state == "menu" and event.key == pygame.K_RETURN:
                    state = "play"
                elif state == "play" and event.key in (pygame.K_w, pygame.K_UP, pygame.K_SPACE):
                    player.jump()
                elif state == "play" and event.key == pygame.K_f and player.can_shoot(now):
                    bullets.append(player.shoot(now))
                elif state in ("victory", "game_over") and event.key == pygame.K_r:
                    level_index = 0
                    level = LevelState(level_index)
                    player = Player(level.player_spawn)
                    bullets = []
                    state = "menu"

        if state == "play":
            keys = pygame.key.get_pressed()
            player.handle_input(keys)
            player.update(level.platforms)

            for enemy in level.enemies:
                if enemy.alive:
                    enemy.update()
            if level.boss and level.boss.alive:
                level.boss.update()

            for pickup in level.pickups:
                if pickup.active and player.rect.colliderect(pickup.rect):
                    player.weapon = pickup.weapon
                    pickup.active = False

            for bullet in bullets:
                bullet.update()
                for enemy in level.enemies:
                    if enemy.alive and bullet.rect.colliderect(enemy.rect):
                        enemy.apply_damage(bullet.damage)
                        bullet.rect.x = -999
                if level.boss and level.boss.alive and bullet.rect.colliderect(level.boss.rect):
                    level.boss.apply_damage(bullet.damage)
                    bullet.rect.x = -999
            bullets = [b for b in bullets if b.alive]

            for enemy in level.enemies:
                if enemy.alive and player.rect.colliderect(enemy.rect):
                    if now - enemy.damage_cooldown > 900:
                        player.hp -= 1
                        enemy.damage_cooldown = now
            if level.boss and level.boss.alive and player.rect.colliderect(level.boss.rect):
                if now - level.boss.damage_cooldown > 700:
                    player.hp -= 1
                    level.boss.damage_cooldown = now

            if player.hp <= 0:
                state = "game_over"

            if level.complete:
                if level.exit and player.rect.colliderect(level.exit.rect):
                    level_index += 1
                    if level_index >= len(LEVELS):
                        state = "victory"
                    else:
                        level = LevelState(level_index)
                        player = Player(level.player_spawn)
                        bullets = []
                elif level.boss and not level.boss.alive:
                    state = "victory"

        screen.fill((20, 24, 36))

        if state == "menu":
            draw_text(screen, "PERQUE FAN GAME", 54, (244, 244, 244), SCREEN_WIDTH // 2, 120, center=True)
            draw_text(screen, "Аркадный платформер: беги, прыгай, стреляй", 28, (200, 200, 220), SCREEN_WIDTH // 2, 200, center=True)
            draw_text(screen, "Управление: A/D, W/↑/Space, F - стрельба", 24, (180, 210, 245), SCREEN_WIDTH // 2, 260, center=True)
            draw_text(screen, "Нажми Enter для старта", 30, (255, 170, 90), SCREEN_WIDTH // 2, 340, center=True)

        elif state == "play":
            for platform in level.platforms:
                pygame.draw.rect(screen, (70, 90, 125), platform)

            if level.exit and level.complete:
                pygame.draw.rect(screen, (95, 200, 140), level.exit.rect)
                draw_text(screen, "EXIT", 18, (20, 30, 20), level.exit.rect.x + 3, level.exit.rect.y + 25)

            for pickup in level.pickups:
                if pickup.active:
                    pygame.draw.rect(screen, (255, 160, 80), pickup.rect)
                    draw_text(screen, pickup.weapon.upper(), 14, (20, 20, 20), pickup.rect.x - 8, pickup.rect.y - 16)

            for enemy in level.enemies:
                if enemy.alive:
                    pygame.draw.rect(screen, (230, 80, 80), enemy.rect)

            if level.boss and level.boss.alive:
                pygame.draw.rect(screen, (180, 60, 220), level.boss.rect)
                draw_text(screen, f"BOSS HP: {level.boss.hp}", 20, (250, 220, 255), 730, 20)

            pygame.draw.rect(screen, (80, 180, 255), player.rect)

            for bullet in bullets:
                pygame.draw.rect(screen, bullet.color, bullet.rect)

            draw_text(screen, level.name, 25, (240, 240, 255), 20, 16)
            draw_text(screen, f"HP: {player.hp}", 25, (255, 110, 120), 20, 46)
            draw_text(screen, f"Оружие: {player.weapon}", 25, (255, 230, 130), 20, 76)
            draw_text(screen, f"FPS: {int(clock.get_fps())}", 18, (170, 170, 190), 850, 16)

        elif state == "victory":
            draw_text(screen, "ПОБЕДА!", 62, (120, 245, 170), SCREEN_WIDTH // 2, 120, center=True)
            draw_text(screen, "Ты прошёл все уровни и победил босса!", 30, (245, 245, 250), SCREEN_WIDTH // 2, 200, center=True)
            draw_text(screen, f"Промокод на скидку в магазине {BRAND_NAME}:", 28, (240, 220, 170), SCREEN_WIDTH // 2, 270, center=True)
            draw_text(screen, PROMO_CODE, 50, (255, 160, 100), SCREEN_WIDTH // 2, 330, center=True)
            draw_text(screen, "Нажми R, чтобы сыграть ещё раз", 25, (200, 200, 220), SCREEN_WIDTH // 2, 420, center=True)

        elif state == "game_over":
            draw_text(screen, "GAME OVER", 62, (255, 90, 90), SCREEN_WIDTH // 2, 170, center=True)
            draw_text(screen, "Герой Perque потерпел поражение", 29, (230, 230, 240), SCREEN_WIDTH // 2, 250, center=True)
            draw_text(screen, "Нажми R для рестарта", 28, (210, 220, 255), SCREEN_WIDTH // 2, 330, center=True)

        pygame.display.flip()


if __name__ == "__main__":
    run()

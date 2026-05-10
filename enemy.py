import pygame
from settings import *


class Enemy(pygame.Rect):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.velocity_y = 0
        self.direction = -1
        self.on_ground = False
        self.last_bullet_time = pygame.time.get_ticks()

    def shoot(self, player, game_):
        if pygame.time.get_ticks() - self.last_bullet_time > 500:
            x = self.x - ENEMY_WIDTH * 20 if self.direction == -1 else self.right
            range_rect = pygame.Rect(
                x, self.y, ENEMY_WIDTH * 20, ENEMY_HEIGHT
            )

            bullet_x = self.x if self.direction == 1 else self.right
            if range_rect.colliderect(player):
                bullet = Projectile(
                    bullet_x, self.centery - 1, 5, 5, self.direction
                )
                game_.bullets.append(bullet)

            self.last_bullet_time = pygame.time.get_ticks()

        for bullet in game_.bullets:
            if bullet.colliderect(player):
                pygame.quit()
                quit()
        for enemy in game_.enemies:
            if enemy.colliderect(player):
                pygame.quit()
                quit()


class Projectile(pygame.Rect):
    def __init__(self, x, y, w, h, direction):
        super().__init__(x, y, w, h)
        self.radius = 5
        self.direction = direction
import pygame
from settings import *
from tilemap import tilemap
from enemy import Enemy


class Game:
    def    __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Platformer")

        self.player = pygame.Rect(
            30, HEIGHT - 120, PLAYER_WIDTH, PLAYER_HEIGHT
        )
        self.velocity_y = 0
        self.on_ground = False

        self.tiles = []
        self.bullets = []
        self.enemies = []
        for enemy_location in ENEMY_LOCATIONS:
            enemy = Enemy(
                enemy_location[0], enemy_location[1], ENEMY_WIDTH, ENEMY_HEIGHT
            )
            self.enemies.append(enemy)


        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == 1:
                    tile = pygame.Rect(
                        j * TILE_WIDTH, i * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT
                    )
                    self.tiles.append(tile)

        self.clock = pygame.time.Clock()

    def move(self):
        dx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dx = -SPEED
        if keys[pygame.K_d]:
            dx = SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = JUMP_FACTOR
            self.on_ground = False


        self.velocity_y += GRAVITY
        dy = self.velocity_y

        self.on_ground = False

        self.player.x += dx
        for tile in self.tiles:
            if self.player.colliderect(tile):
                if dx > 0:
                    self.player.right = tile.left
                if dx < 0:
                    self.player.left = tile.right

        self.player.y += dy
        for wall in self.tiles:
            if self.player.colliderect(wall):
                if dy > 0:
                    self.player.bottom = wall.top
                    self.velocity_y = 0
                    self.on_ground = True
                if dy < 0:
                    self.player.top = wall.bottom
                    self.velocity_y = 0

        # enemy movements
        for enemy in self.enemies:
            # attack
            enemy.shoot(self.player, self)

            enemy.velocity_y += GRAVITY

            # enemy y-movement
            edy = enemy.velocity_y
            enemy.y += edy
            enemy.on_ground = False

            for tile_ in self.tiles:
                if enemy.colliderect(tile_):
                    if edy > 0:
                        enemy.bottom = tile_.top
                        enemy.velocity_y = 0
                        enemy.on_ground = True

            # check edges
            if enemy.direction == 1:
                check_x = enemy.right + 1
            else:
                check_x = enemy.left - 1

            check_y = enemy.bottom + 1
            ground_ahead = False
            for t in self.tiles:
                if t.collidepoint(check_x, check_y):
                    ground_ahead = True
                    break

            if not ground_ahead:
                enemy.direction *= -1

            # enemy x-movement
            edx = ENEMY_SPEED * enemy.direction
            enemy.x += edx
            for wall_ in self.tiles:
                if enemy.colliderect(wall_):
                    if edx > 0:
                        enemy.right = wall_.left
                        enemy.direction = -1
                    if edx < 0:
                        enemy.left = wall_.right
                        enemy.direction = 1

        for bullet in self.bullets:
            bullet.x += PROJECTILE_SPEED * bullet.direction

    def draw(self):
        self.screen.fill(BLACK)

        pygame.draw.rect(self.screen, RED, self.player)

        for tile in self.tiles:
            pygame.draw.rect(
                self.screen, TILE_COLOR, tile
            )

        for enemy in self.enemies:
            pygame.draw.rect(
                self.screen, GREEN, enemy
            )

        for bullet in self.bullets:
            pygame.draw.circle(
                self.screen, YELLOW, bullet.center, bullet.radius
            )

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.move()
            self.draw()

            self.clock.tick(FPS)

        pygame.quit()
        quit()


if __name__ == "__main__":
    Game().run()
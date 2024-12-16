import asyncio
import random
import pygame

# Размеры окна
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Параметры игрока и препятствий
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
PLAYER_SPEED = 1
OBSTACLE_SPEED = 5


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.obstacles = []
        self.score = 0

    async def draw(self):
        while self.running:
            self.screen.fill(WHITE)

            # Рисуем игрока
            pygame.draw.rect(self.screen, GREEN, (self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

            # Рисуем препятствия
            for obstacle_x, obstacle_y in self.obstacles:
                pygame.draw.rect(self.screen, RED, (obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

            # Отображаем счёт
            font = pygame.font.SysFont(None, 36)
            score_text = font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            await asyncio.sleep(0)

    async def move_player(self):
        while self.running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_x > 0:
                self.player_x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and self.player_x < SCREEN_WIDTH - PLAYER_WIDTH:
                self.player_x += PLAYER_SPEED

            await asyncio.sleep(0)

    async def spawn_obstacles(self):
        while self.running:
            obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
            self.obstacles.append([obstacle_x, 0])
            await asyncio.sleep(1)

    async def update_obstacles(self):
        while self.running:
            for obstacle in self.obstacles:
                obstacle[1] += OBSTACLE_SPEED

                # Проверяем столкновение с игроком
                if (self.player_y < obstacle[1] + OBSTACLE_HEIGHT and
                        self.player_y + PLAYER_HEIGHT > obstacle[1] and
                        self.player_x < obstacle[0] + OBSTACLE_WIDTH and
                        self.player_x + PLAYER_WIDTH > obstacle[0]):
                    self.running = False

            # Удаляем препятствия за пределами экрана
            self.obstacles = [obs for obs in self.obstacles if obs[1] < SCREEN_HEIGHT]

            # Увеличиваем счёт
            self.score += 1
            await asyncio.sleep(0.05)

    async def check_events(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            await asyncio.sleep(0)

    async def main(self):
        draw_task = asyncio.create_task(self.draw())
        player_task = asyncio.create_task(self.move_player())
        spawn_task = asyncio.create_task(self.spawn_obstacles())
        update_task = asyncio.create_task(self.update_obstacles())
        events_task = asyncio.create_task(self.check_events())

        await asyncio.gather(draw_task, player_task, spawn_task, update_task, events_task)

    def run(self):
        asyncio.run(self.main())
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()

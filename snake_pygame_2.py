import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define game constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# Initialize the game window
game_window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Snake Game')

# Define game objects
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def move(self):
        cur = self.positions[-1]
        x, y = cur

        if self.direction == UP:
            y -= 10
        elif self.direction == DOWN:
            y += 10
        elif self.direction == LEFT:
            x -= 10
        elif self.direction == RIGHT:
            x += 10

        self.positions.append((x, y))
        self.positions = self.positions[-self.length:]

    def change_direction(self, dir):
        if dir == UP and self.direction != DOWN:
            self.direction = UP
        elif dir == DOWN and self.direction != UP:
            self.direction = DOWN
        elif dir == LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif dir == RIGHT and self.direction != LEFT:
            self.direction = RIGHT

    def draw(self, game_window):
        for pos in self.positions:
            pygame.draw.rect(game_window, WHITE, pygame.Rect(pos[0], pos[1], 10, 10))


class Food:
    def __init__(self):
        self.pos = None

        self.place()

    def place(self):
        x = random.randint(0, DISPLAY_WIDTH - 10)
        y = random.randint(0, DISPLAY_HEIGHT - 10)
        self.pos = (x, y)

    def draw(self, game_window):
        pygame.draw.rect(game_window, RED, pygame.Rect(self.pos[0], self.pos[1], 10, 10))

    def eat(self, snake):
        if snake.positions[0] == self.pos:
            return True
        return False


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0

    def play(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    if event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    if event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    if event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)

            game_window.fill(BLACK)
            self.snake.move()
            self.snake.draw(game_window)
            if self.food.eat(self.snake):
                self.score += 1
                self.food.place()
            self.food.draw(game_window)
            pygame.display.update()
            clock.tick(10)


if __name__ == '__main__':
    game = Game()
    game.play()
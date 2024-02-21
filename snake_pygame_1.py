import sys
import random
from time import sleep
import pygame as pg

# Constants
FPS = 10   # Frames per Second
SIZE = WIDTH, HEIGHT = 640, 480    # Window Size
CELL_SIZE = 10     # Grid Cell Size
WHITE = (255, 255, 255)      # Color White
BLACK = (0, 0, 0)        # Color Black
RED = (255, 0, 0)            # Color Red
GREEN = (0, 255, 0)          # Color Green

snake_speed = CELL_SIZE * 2      # Initial Speed
snake_body = [(int((WIDTH / 2) // CELL_SIZE) * CELL_SIZE, int((HEIGHT / 2) // CELL_SIZE) * CELL_SIZE)]   # Starting Position
dir_x, dir_y = 0, 0               # Movement Direction
score = 0                         # Player Score
running = True                     # Keep Track Of Running Status
pause = False                      # Keep Track Of Pause Status


def get_apple_location():
    while True:
        x = random.randrange(0, WIDTH - CELL_SIZE + 1, CELL_SIZE)
        y = random.randrange(0, HEIGHT - CELL_SIZE + 1, CELL_SIZE)
        new_pos = (x, y)
        if len(list(filter(lambda z: z == new_pos, snake_body))) > 0:
            continue        # Try Again If Position Is Occupied By Snake Body
        else:
            break
    return new_pos


apple_pos = get_apple_location()      # Apple Location

def main():
    global SCREEN, CLOCK
    pg.init()       # Initialize PyGame Module
    SCREEN = pg.display.set_mode(SIZE)         # Create Main Surface
    pg.display.set_caption("PySnake")              # Set Title Bar Text
    CLOCK = pg.time.Clock()                    # Control Frame Rate
    show_start_screen()           # Show Start Screen
    while True:                # Run Until User Quit
        run_game()             # Play One Round Of Snake Game
        show_end_screen()          # Show End Screen

def show_start_screen():
    pass    # TODO: Implement start screen

def show_end_screen():
    pass    # TODO: Implement end screen

def run_game():

    while running:
        for event in pg.event.get():        # Handle Events From Keyboard And Mouse
            if event.type == pg.QUIT:       # Check For Close Button Click Event
                terminate()             # Exit Program
            elif event.type == pg.KEYDOWN:      # Check For Arrow Keys Input
                if event.key == pg.K_ESCAPE:    # Escape Key Stops The Game
                    terminate()             # Exit Program
                elif event.key == pg.K_SPACE:   # Spacebar Toggles Pause State
                    pause = not pause          # Switch Between Paused And Unpaused States
                else:
                    if not pause:          # Only Change Directions When Not Paused
                        if event.key == pg.K_LEFT and dir_x != CELL_SIZE:
                            dir_x = -CELL_SIZE
                            dir_y = 0
                        elif event.key == pg.K_RIGHT and dir_x != -CELL_SIZE:
                            dir_x = CELL_SIZE
                            dir_y = 0
                        elif event.key == pg.K_UP and dir_y != CELL_SIZE:
                            dir_x = 0
                            dir_y = -CELL_SIZE
                        elif event.key == pg.K_DOWN and dir_y != -CELL_SIZE:
                            dir_x = 0
                            dir_y = CELL_SIZE

        if not pause:
            old_segment = snake_body[-1]        # Store Last Segment Before Updating It
            del snake_body[-1]                  # Remove Last Segment
            new_coord = ((snake_body[0][0] + dir_x) % WIDTH, (snake_body[0][1] + dir_y) % HEIGHT)   # Calculate New Head Coordinates
            snake_body.insert(0, new_coord)     # Insert New Head At Beginning Of List

            # Detect Collision With Self Or Wall
            if snake_body[0] in snake_body[1:] or \
                    snake_body[0][0] < 0 or snake_body[0][0] >= WIDTH or\
                    snake_body[0][1] < 0 or snake_body[0][1] >= HEIGHT:
                return score       # Return Final Score On Collision

            # Eat Apples By Changing Its Location
            if snake_body[0] == apple_pos:
                snake_body.append(old_segment)  # Add Back Removed Segment
                apple_pos = get_apple_location()    # Generate New Random Apple Location
                score += 1                      # Update Score

            clear_screen()                  # Clear Previous Drawings
            draw_objects(score, apple_pos)      # Render All Objects Again

        clock.tick(fps)                     # Limit Frame Rate


def clear_screen():
    SCREEN.fill(BLACK)        # Erase Everything On The Screen

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):       # Vertical Lines
        pg.draw.line(SCREEN, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):      # Horizontal Lines
        pg.draw.line(SCREEN, WHITE, (0, y), (WIDTH, y))

def draw_snake(segments):
    for pos in segments:
        rect = pg.Rect((pos[0], pos[1]), (CELL_SIZE, CELL_SIZE))
        pg.draw.rect(SCREEN, GREEN, rect)
        inside_rect = pg.Rect((pos[0] + 4, pos[1] + 4), (CELL_SIZE - 8, CELL_SIZE - 8))
        pg.draw.rect(SCREEN, BLACK, inside_rect)

def draw_text(text, size, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    SCREEN.blit(text_surface, text_rect)

def draw_objects(score, apple_pos):
    draw_grid()            # Background Grid
    draw_snake(snake_body)     # Snake Body
    draw_apple(apple_pos)      # Apple
    draw_score(score)          # Current Score Value
    pg.display.update()        # Refresh Display

def draw_apple(pos):
    radius = int(CELL_SIZE * 0.45)
    pg.draw.circle(SCREEN, RED, (pos[0] + CELL_SIZE // 2, pos[1] + CELL_SIZE // 2), radius)

def draw_score(value):
    draw_text('Score: {}'.format(value), 28, WIDTH // 2, 10)

if __name__ == '__main__':
    main()
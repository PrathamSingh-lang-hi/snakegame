import pygame
import random

# Initialize pygame
pygame.init()

# Set display width and height
width, height = 900, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Snake settings
block_size = 10
speed = 10

# Font and clock
font = pygame.font.SysFont("bahnschrift", 25)
clock = pygame.time.Clock()

def message(msg, color, x, y):
    """Display a message on the screen."""
    text = font.render(msg, True, color)
    win.blit(text, [x, y])

def game_loop():
    """Main game loop."""
    game_over = False
    game_close = False

    x, y = width / 2, height / 2
    x_change, y_change = 0, 0

    snake = []
    length = 1

    food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0

    while not game_over:
        while game_close:
            win.fill(black)
            message("Game Over! Press Q to Quit or C to Play Again", red, width / 6, height / 3)
            pygame.display.update()     

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0

        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        win.fill(blue)

        pygame.draw.rect(win, green, [food_x, food_y, block_size, block_size])
        snake.append((x, y))
        if len(snake) > length:
            del snake[0]

        for segment in snake[:-1]:
            if segment == (x, y):
                game_close = True

        for pos in snake:
            pygame.draw.rect(win, white, [pos[0], pos[1], block_size, block_size])

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
            length += 1

        clock.tick(speed)

    pygame.quit()
    quit()

# Run the game
game_loop()
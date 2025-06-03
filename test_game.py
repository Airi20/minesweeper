import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

#click_sound = pygame.mixer.Sound("クリック.mp3")
#explosion_sound = pygame.mixer.Sound("爆発1.mp3")

WIDTH, HEIGHT = 440, 540
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
PINK = (255, 192, 203)

ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS
NUM_BOMBS = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("親愛なる妹へ")
font = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 48)

reset_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 35, 100, 30)

def place_bombs():
    bombs = set()
    while len(bombs) < NUM_BOMBS:
        bombs.add((random.randint(0, COLS - 1), random.randint(0, ROWS - 1)))
    return bombs

def count_bombs_around(x, y, bombs):
    count = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            nx, ny = x + dx, y + dy
            if (dx != 0 or dy != 0) and (0 <= nx < COLS) and (0 <= ny < ROWS):
                if (nx, ny) in bombs:
                    count += 1
    return count

def reveal_cell(x, y, bombs, revealed):
    if not (0 <= x < COLS and 0 <= y < ROWS):
        return
    if revealed[y][x]:
        return

    revealed[y][x] = True

    if (x, y) in bombs:
        return

    if count_bombs_around(x, y, bombs) == 0:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx != 0 or dy != 0:
                    reveal_cell(x + dx, y + dy, bombs, revealed)

def check_clear(bombs, revealed):
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) not in bombs and not revealed[y][x]:
                return False
    return True

def reset_game():
    return place_bombs(), [[False] * COLS for _ in range(ROWS)], False, False

bombs, revealed, game_over, win = reset_game()

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if reset_button_rect.collidepoint(mx, my):
                bombs, revealed, game_over, win = reset_game()
            elif not game_over:
                x = mx // CELL_SIZE
                y = my // CELL_SIZE
                if 0 <= x < COLS and 0 <= y < ROWS and not revealed[y][x]:
                    if (x, y) in bombs:
                        #explosion_sound.play()
                        revealed[y][x] = True
                        game_over = True
                        win = False
                    else:
                        #click_sound.play()
                        reveal_cell(x, y, bombs, revealed)
                        if check_clear(bombs, revealed):
                            game_over = True
                            win = True

    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[y][x]:
                pygame.draw.rect(screen, GRAY, rect)
                if (x, y) in bombs:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                else:
                    count = count_bombs_around(x, y, bombs)
                    if count > 0:
                        text = font.render(str(count), True, BLACK)
                        screen.blit(text, (x * CELL_SIZE + 10, y * CELL_SIZE + 5))
            else:
                pygame.draw.rect(screen, BLACK, rect, 1)

    pygame.draw.rect(screen, PINK, reset_button_rect)
    text = font.render("リセット", True, BLACK)
    screen.blit(text, (reset_button_rect.x + 20, reset_button_rect.y + 5))

    if game_over:
        if win:
            text = font_large.render("You Win!", True, (0, 128, 0))
        else:
            text = font_large.render("Game Over", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()

pygame.quit()

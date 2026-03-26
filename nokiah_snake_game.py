# Nokiah Snake-Game
# (mobile-friendly)


import pygame
import random
import sys
import os

pygame.init()

# Screen setup
WIDTH = 600
HEIGHT = 750
GAME_HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nokiah Snake-Game")

clock = pygame.time.Clock()

# Snake block
SNAKE_BLOCK = 20

# Fonts
font = pygame.font.SysFont("arial", 30)
big_font = pygame.font.SysFont("arial", 50)

# High score file
HS_FILE = "highscore.txt"

# Themes
THEMES = {
    "Dark": {"snake": (0, 255, 0), "food": (255, 0, 0), "bg": (18, 18, 18), "button": (80,80,80)},
    "Neon": {"snake": (0,255,255), "food": (255,0,255), "bg": (0,0,0), "button": (255,255,0)},
    "Retro": {"snake": (255,128,0), "food": (0,0,255), "bg": (230,230,180), "button": (128,77,0)}
}

# Buttons positions
BTN_UP = pygame.Rect(250, 630, 100, 50)
BTN_DOWN = pygame.Rect(250, 690, 100, 50)
BTN_LEFT = pygame.Rect(130, 660, 100, 50)
BTN_RIGHT = pygame.Rect(370, 660, 100, 50)
BTN_RESTART = pygame.Rect(200, 350, 200, 60)

# Helper functions
def load_high_score():
    if os.path.exists(HS_FILE):
        with open(HS_FILE,"r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(HS_FILE,"w") as f:
        f.write(str(score))

# Draw buttons
def draw_buttons(theme):
    pygame.draw.rect(screen, theme["button"], BTN_UP, border_radius=10)
    pygame.draw.rect(screen, theme["button"], BTN_DOWN, border_radius=10)
    pygame.draw.rect(screen, theme["button"], BTN_LEFT, border_radius=10)
    pygame.draw.rect(screen, theme["button"], BTN_RIGHT, border_radius=10)
    screen.blit(font.render("UP", True, (255,255,255)), (285,640))
    screen.blit(font.render("DOWN", True, (255,255,255)), (260,700))
    screen.blit(font.render("LEFT", True, (255,255,255)), (155,670))
    screen.blit(font.render("RIGHT", True, (255,255,255)), (390,670))

# Draw snake
def draw_snake(snake_list, theme):
    for block in snake_list:
        pygame.draw.rect(screen, theme["snake"], [block[0], block[1], SNAKE_BLOCK, SNAKE_BLOCK], border_radius=5)

# Draw score
def draw_score(score, high_score, y_offset=0):
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (20,10 + y_offset))
    screen.blit(font.render(f"High Score: {high_score}", True, (70,130,180)), (350,10 + y_offset))

# Difficulty selection screen
def select_difficulty():
    while True:
        screen.fill((30,30,30))
        screen.blit(big_font.render("Nokiah Snake-Game", True, (255,255,255)), (120,100))
        screen.blit(big_font.render("Select Difficulty", True, (255,255,255)), (130,200))
        easy_btn = pygame.Rect(200,300,200,60)
        medium_btn = pygame.Rect(200,400,200,60)
        hard_btn = pygame.Rect(200,500,200,60)
        pygame.draw.rect(screen, (0,255,0), easy_btn)
        pygame.draw.rect(screen, (255,255,0), medium_btn)
        pygame.draw.rect(screen, (255,0,0), hard_btn)
        screen.blit(font.render("EASY", True, (0,0,0)), (260,315))
        screen.blit(font.render("MEDIUM", True, (0,0,0)), (240,415))
        screen.blit(font.render("HARD", True, (0,0,0)), (260,515))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(event.pos):
                    return 5
                if medium_btn.collidepoint(event.pos):
                    return 10
                if hard_btn.collidepoint(event.pos):
                    return 15

# Theme selection screen
def select_theme():
    while True:
        screen.fill((30,30,30))
        # Center game name horizontally
        game_name = big_font.render("Nokiah Snake-Game", True, (255,255,255))
        screen.blit(game_name, ((WIDTH - game_name.get_width()) // 2, 100))
        screen.blit(big_font.render("Select Theme", True, (255,255,255)), (180,200))
        
        dark_btn = pygame.Rect(100,300,120,60)
        neon_btn = pygame.Rect(240,300,120,60)
        retro_btn = pygame.Rect(380,300,120,60)
        pygame.draw.rect(screen, (50,50,50), dark_btn)
        pygame.draw.rect(screen, (0,255,255), neon_btn)
        pygame.draw.rect(screen, (255,128,0), retro_btn)
        screen.blit(font.render("DARK", True, (255,255,255)), (120,315))
        screen.blit(font.render("NEON", True, (0,0,0)), (260,315))
        screen.blit(font.render("RETRO", True, (0,0,0)), (400,315))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if dark_btn.collidepoint(event.pos):
                    return THEMES["Dark"]
                if neon_btn.collidepoint(event.pos):
                    return THEMES["Neon"]
                if retro_btn.collidepoint(event.pos):
                    return THEMES["Retro"]

# Main game loop
def game():
    snake_speed = select_difficulty()
    theme = select_theme()

    x = WIDTH//2
    y = GAME_HEIGHT//2
    x_change = 0
    y_change = 0
    snake_list = []
    length = 1

    foodx = random.randrange(0, WIDTH-SNAKE_BLOCK, SNAKE_BLOCK)
    foody = random.randrange(0, GAME_HEIGHT-SNAKE_BLOCK, SNAKE_BLOCK)

    score = 0
    high_score = load_high_score()
    game_over = False

    while True:
        screen.fill(theme["bg"])

        # Draw game area box
        pygame.draw.rect(screen, (255,255,255), (0,0,WIDTH,GAME_HEIGHT), 3)

        # Draw game name at top, centered horizontally
        game_name_text = font.render("Nokiah Snake-Game", True, (255,255,255))
        screen.blit(game_name_text, ((WIDTH - game_name_text.get_width()) // 2, 10))

        # Draw score below game name with spacing
        draw_score(score, high_score, y_offset=40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_UP.collidepoint(event.pos) and y_change == 0:
                    x_change = 0
                    y_change = -SNAKE_BLOCK
                if BTN_DOWN.collidepoint(event.pos) and y_change == 0:
                    x_change = 0
                    y_change = SNAKE_BLOCK
                if BTN_LEFT.collidepoint(event.pos) and x_change == 0:
                    x_change = -SNAKE_BLOCK
                    y_change = 0
                if BTN_RIGHT.collidepoint(event.pos) and x_change == 0:
                    x_change = SNAKE_BLOCK
                    y_change = 0
                if game_over and BTN_RESTART.collidepoint(event.pos):
                    return game()

        if not game_over:
            x += x_change
            y += y_change

            # Collision with walls
            if x < 0 or x >= WIDTH or y < 0 or y >= GAME_HEIGHT:
                game_over = True

            snake_head = [x,y]
            snake_list.append(snake_head)
            if len(snake_list) > length:
                del snake_list[0]

            # Self-collision
            for block in snake_list[:-1]:
                if block == snake_head:
                    game_over = True

            # Food collision
            pygame.draw.rect(screen, theme["food"], [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])
            if x == foodx and y == foody:
                length +=1
                score +=1
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                foodx = random.randrange(0, WIDTH-SNAKE_BLOCK, SNAKE_BLOCK)
                foody = random.randrange(0, GAME_HEIGHT-SNAKE_BLOCK, SNAKE_BLOCK)

            draw_snake(snake_list, theme)
            draw_buttons(theme)

        else:
            screen.blit(big_font.render("GAME OVER", True, (255,0,0)), (150,250))
            pygame.draw.rect(screen, theme["button"], BTN_RESTART, border_radius=15)
            screen.blit(font.render("RESTART", True, (255,255,255)), (240,370))

        pygame.display.update()
        clock.tick(snake_speed)

game()

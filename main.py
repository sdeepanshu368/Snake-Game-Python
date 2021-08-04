# Importing The Modules
import random
import os
import pygame
from pygame import mixer

# Initialization
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (35, 45, 40)

# Game Backgrounds
bg1 = pygame.image.load("Screen/bg1.jpg")
bg2 = pygame.image.load("Screen/bg2.jpg")
bg3 = pygame.image.load("Screen/bg3.jpg")
intro = pygame.image.load("Screen/intro.jpg")
outro = pygame.image.load("Screen/outro.jpg")

# Creating The window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()

# Variables For The Game
clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington', 35)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


# Welcome Screen
def welcome():
    # mixer.music.load(os.path.join(os.getcwd(), 'Music', 'back.mp3'))
    mixer.music.load(os.path.join(os.getcwd(), 'Music', 'back.wav'))
    mixer.music.set_volume(.5)
    mixer.music.play(-1)

    exit_game = False
    while not exit_game:
        gameWindow.blit(intro, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    # Highscore Build
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    # Food
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    # Game Variables
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            # GameOverScreen
            gameWindow.blit(outro, (0, 0))
            text_screen("Score: " + str(score), green, 385, 325)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    moveSound = mixer.Sound('Music\\move.mp3')
                    moveSound.play()
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score +=10
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            if abs(snake_x - food_x)<20 and abs(snake_y - food_y)<20:
                foodSound = mixer.Sound('Music\\food.mp3')
                foodSound.play()
                score +=10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
                if score>int(highscore):
                    highscore = score
            gameWindow.blit(bg3, (0, 0))
            text_screen("Score: " + str(score) + "  Highscore: "+str(highscore),  green, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                game_over = True
                gameOverSound = mixer.Sound('Music\\gameover.mp3')
                gameOverSound.play()
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                gameOverSound = mixer.Sound('Music\\gameover.mp3')
                gameOverSound.play()
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


welcome()

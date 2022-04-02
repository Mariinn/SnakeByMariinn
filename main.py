#pip install pygame в терминале
import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
pygame.display.set_caption('Snake')
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

pygame.mixer.init()

game_sound = pygame.mixer.Sound("gamesound.wav")
game_sound.set_volume(0.6)
point_sound = pygame.mixer.Sound("point.wav")
point_sound.set_volume(0.4)


# r =  Rect( left, top, width, hight )
#head = Rect(400, 300, 30, 30)
game_points = 0
speed = 30
direction = [speed, 0]
color = (255, 255, 255)




def load_image(src, x, y):
    image = pygame.image.load(src).convert()
    image = pygame.transform.scale(image, (30, 30))
    rect = image.get_rect(center=(x, y))

    transparent = image.get_at((0, 0))
    image.set_colorkey(transparent)

    return image, rect

def random_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return(r, g, b)

def move(head, snake):
    global direction, color

    if keys[K_w] and direction[1] == 0:
        direction = [0, -speed]
    elif keys[K_s] and direction[1] == 0:
        direction = [0, speed]
    elif keys[K_d] and direction[0] == 0:
        direction = [speed, 0]
    elif keys[K_a] and direction[0] == 0:
        direction = [-speed, 0]


    if head.bottom > 600:
        # direction = [0, -speed]
        head.top = 0
    elif head.top < 0:
        # direction = [0, speed]
        head.bottom = 600
    elif head.left < 0:
        # direction = [speed, 0]
        head.right = 800
    elif head.right > 800:
        # direction = [-speed, 0]
        head.left = 0

    for index in range(len(snake)-1, 0, -1):
        snake[index].x = snake[index-1].x
        snake[index].y = snake[index-1].y

    head.move_ip((direction))

def pickup():
    global apple_rect, head_rect, heart_rect, game_points, snake

    if head_rect.colliderect(apple_rect):
        apple_rect.x = randint(40, 760)
        apple_rect.y = randint(40, 560)
        game_points += 10
        print(f'game_points: {game_points}')
        snake.append(snake[-1].copy())
        point_sound.play()
    if head_rect.colliderect(heart_rect):
        heart_rect.x = randint(40, 760)
        heart_rect.y = randint(40, 560)
        game_points += 10
        print(f'game_points: {game_points}')
        snake.append(snake[-1].copy())
        point_sound.play()

def score():
    global game_points
    text = font.render(f'Score: {game_points}', True, (216, 250, 200))
    text_rect = text.get_rect(center=(400, 500))
    screen.blit(text, text_rect)

def gameover():
    global snake, head_rect
    for segment in snake[1:]:
        if head_rect.colliderect(segment):
            return True
    return False
head_image, head_rect = load_image('head.png', 400, 300)
apple_image, apple_rect = load_image('apple.png', 200, 300)
heart_image, heart_rect = load_image('heart.png', 200, 300)
body_image, body_rect = load_image('body.png', 400, 300)

snake = [head_rect, body_rect]

game_sound.play()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    # pygame.draw.rect(screen, (color), head)

    screen.blit(head_image, head_rect)
    screen.blit(apple_image, apple_rect)
    screen.blit(heart_image, heart_rect)

    for segment in snake[1:]:
        screen.blit(body_image, segment)

    move(head_rect, snake)
    pickup()
    score()

    if gameover():
        pygame.quit()
        exit()
    pygame.display.update()
    clock.tick(20)

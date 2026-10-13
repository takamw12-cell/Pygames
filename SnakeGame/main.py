import pygame
import random

pygame.init()

font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

# creer la fenetre du jeu
screen = pygame.display.set_mode((600, 400))
# Donner un titre a la fenetre
pygame.display.set_caption("Mon jeu Snake")
# couleur noir
black = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# position du serpent

snake_x = 300
snake_y = 200
size = 20

score = 0

snake_body = []
snake_length = 1

speed_x = 0
speed_y = 0

apple_x = 100
apple_y = 100

# garder la fenetre ouverte
running = True

game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and speed_x == 0:
                speed_x = 20
                speed_y = 0

            if event.key == pygame.K_LEFT and speed_x == 0:
                speed_x = -20
                speed_y = 0

            if event.key == pygame.K_UP and speed_y == 0:
                speed_x = 0
                speed_y = -20

            if event.key == pygame.K_DOWN and speed_y == 0:
                speed_x = 0
                speed_y = 20

            if event.key == pygame.K_r and game_over:
                snake_x = 300
                snake_y = 200
                size = 20

                score = 0

                snake_body = []
                snake_length = 1

                speed_x = 0
                speed_y = 0

                apple_x = 100
                apple_y = 100

                game_over = False

    if not game_over:
        snake_x += speed_x
        snake_y += speed_y
        if snake_x < 0 or snake_x >= 600 or snake_y < 0 or snake_y >= 400:
            game_over = True

    snake_head = [snake_x, snake_y]
    snake_body.append(snake_head)

    if len(snake_body) > snake_length:
        del snake_body[0]

    if snake_head in snake_body[:-1]:
        game_over = True
    screen.fill(black)

    if snake_x == apple_x and snake_y == apple_y:
        snake_length += 1
        score += 1

        apple_x = random.randrange(0, 600, 20)

        apple_y = random.randrange(0, 400, 20)

    pygame.draw.rect(screen, RED, (apple_x, apple_y, size, size))

    for part in snake_body:
        pygame.draw.rect(screen, GREEN, (part[0], part[1], size, size))

    pygame.draw.rect(screen, GREEN, (snake_x, snake_y, size, size))

    score_text = font.render(f"Score : {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    if game_over:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (200, 170))
        pygame.display.flip()

        pygame.time.wait(2000)

    clock.tick(5)

pygame.quit()

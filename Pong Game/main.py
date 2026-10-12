import pygame
import random


# 1. initialiser Pygame
pygame.init()

pygame.mixer.init()
bounce_sound = pygame.mixer.Sound("Pong Game/sounds/bounce.wav")
win_sound = pygame.mixer.Sound("Pong Game/sounds/bounce.wav")
win_sound.set_volume(0.7)
bounce_sound.set_volume(0.5)


# 2. Definir la taille de la fenêtre
WIDTH = 800
HEIGHT = 600
BLACK = (8, 10, 25)
WHITE = (240, 245, 255)
CYAN = (0, 245, 255)
PURPLE = (170, 70, 255)


# ---Menu Principal---
game_started = False
show_controls = False

menu_font = pygame.font.Font(None, 50)
menu_title_font = pygame.font.Font(None, 100)
menu_small_font = pygame.font.Font(None, 30)


def draw_menu():
    screen.fill(BLACK)
    # Titre du jeu
    title = menu_title_font.render("PONG", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

    # Options du menu
    options = ["JOUER", "COMMANDES", "QUITTER"]
    for i, option in enumerate(options):
        color = (255, 220, 80) if i == menu_selection else WHITE
        text = menu_font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 300 + i * 65))

    hint = menu_small_font.render(
        "Utilise les fleches pour naviguer et ENTREE pour selectionner", True, WHITE
    )
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 60))

    pygame.display.flip()


def draw_controls():
    screen.fill(BLACK)
    # Titre
    title = menu_title_font.render("COMMANDES", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))

    # Commandes du joueur gauche
    left_title = menu_font.render("Joueur Gauche", True, (255, 220, 80))
    screen.blit(left_title, (90, 200))

    left_keys = [
        "W : Monter",
        "S : Descendre",
    ]
    for i, line in enumerate(left_keys):
        text = menu_small_font.render(line, True, WHITE)
        screen.blit(text, (110, 270 + i * 45))

    # Commandes du joueur droit
    right_title = menu_font.render("Joueur Droit", True, (255, 220, 80))
    screen.blit(right_title, (450, 200))

    right_keys = [
        "Flèche Haut : Monter",
        "Flèche Bas : Descendre",
    ]
    for i, line in enumerate(right_keys):
        text = menu_small_font.render(line, True, WHITE)
        screen.blit(text, (450, 270 + i * 45))

    # Commandes générales
    general = [
        "EnTREE : choisir dans le menu",
        "R : Recommencer après une Victoire",
        "ECHAP : retour au menu principal",
    ]
    for i, line in enumerate(general):
        text = menu_small_font.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 410 + i * 40))

    pygame.display.flip()


menu_selection = 0


# 3. Créer la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mon premier Pong")

# 4. Définir les couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 4. créer la balle
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_radius = 10

# 5. vitesse de la balle
ball_speed_x = 5
ball_speed_y = 5

BALL_SPEED_INCREASE = 1.05
MAX_BALL_SPEED = 12

# Score des joueurs
score_left = 0
score_right = 0

# Police pour afficher le score
font = pygame.font.Font(None, 60)

# Dimensions des raquettes
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 6

# Position de la raquette gauche
left_paddle = pygame.Rect(
    30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
)

# Position de la raquette droite
right_paddle = pygame.Rect(
    WIDTH - 30 - PADDLE_WIDTH,
    HEIGHT // 2 - PADDLE_HEIGHT // 2,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)

clock = pygame.time.Clock()

running = True

game_over = False

while running:
    # 5. Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and show_controls:
            if event.key == pygame.K_ESCAPE:
                show_controls = False

        elif event.type == pygame.KEYDOWN and not game_started:
            if event.key == pygame.K_UP:
                menu_selection = (menu_selection - 1) % 3
            elif event.key == pygame.K_DOWN:
                menu_selection = (menu_selection + 1) % 3
            elif event.key == pygame.K_RETURN:
                if menu_selection == 0:  # JOUER
                    game_started = True
                    show_controls = False

                elif menu_selection == 1:  # COMMANDES
                    show_controls = True
                elif menu_selection == 2:  # QUITTER
                    running = False

        # Recommencer avec la touche R
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                score_left = 0
                score_right = 0

                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2

                ball_speed_x = 5
                ball_speed_y = 5

                left_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
                right_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2

                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if show_controls:
            draw_controls()
        elif not game_started:
            draw_menu()
        else:
            if not game_over:
                keys = pygame.key.get_pressed()
                # Joueur gauche (W et S)
                if keys[pygame.K_w] and left_paddle.top > 0:
                    left_paddle.y -= PADDLE_SPEED

                if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
                    left_paddle.y += PADDLE_SPEED

                # Joueur droit (flèches haut et bas)
                if keys[pygame.K_UP] and right_paddle.top > 0:
                    right_paddle.y -= PADDLE_SPEED

                if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                    right_paddle.y += PADDLE_SPEED

                # Déplacer la balle
                ball_x += ball_speed_x
                ball_y += ball_speed_y

                # Rebondir sur les murs haut et bas
                if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
                    ball_speed_y = -ball_speed_y

                # Collision avec la raquette de gauche
                ball_rect = pygame.Rect(
                    ball_x - ball_radius,
                    ball_y - ball_radius,
                    ball_radius * 2,
                    ball_radius * 2,
                )

                if ball_rect.colliderect(left_paddle) and ball_speed_x < 0:
                    bounce_sound.play()
                    ball_speed_x = min(
                        abs(ball_speed_x) * BALL_SPEED_INCREASE, MAX_BALL_SPEED
                    )
                    ball_speed_y = (ball_y - left_paddle.centery) * 0.15

                    ball_speed_y = max(
                        -6, min(6, ball_speed_y)
                    )  # Limiter la vitesse verticale

                # Collision avec la raquette de droite
                if ball_rect.colliderect(right_paddle) and ball_speed_x > 0:
                    bounce_sound.play()
                    ball_speed_x = -min(
                        abs(ball_speed_x) * BALL_SPEED_INCREASE, MAX_BALL_SPEED
                    )

                    ball_speed_y = (ball_y - right_paddle.centery) * 0.15
                    ball_speed_y = max(
                        -6, min(6, ball_speed_y)
                    )  # Limiter la vitesse verticale

                # si la balle sort de la gauche, le joueur droit marque un point
                if ball_x + ball_radius < 0:
                    score_right += 1
                    bounce_sound.play()
                    print("Score droite :", score_right)
                    ball_x = WIDTH // 2
                    ball_y = HEIGHT // 2
                    ball_speed_x = 5
                    ball_speed_y = 5

                # si la balle sort de la droite, le joueur gauche marque un point
                elif ball_x - ball_radius > WIDTH:
                    score_left += 1
                    bounce_sound.play()

                    print("Score gauche :", score_left)
                    ball_x = WIDTH // 2
                    ball_y = HEIGHT // 2
                    ball_speed_x = -5
                    ball_speed_y = 4

                if score_left >= 10 or score_right >= 10:
                    game_over = True
                    win_sound.play()

                # Dessiner le fond et la balle
            screen.fill(BLACK)
            for y in range(0, HEIGHT, 30):
                pygame.draw.line(
                    screen, (0, 70, 80), (WIDTH // 2, y), (WIDTH // 2, y + 15), 9
                )
                pygame.draw.line(screen, CYAN, (WIDTH // 2, y), (WIDTH // 2, y + 15), 3)

            pygame.draw.rect(screen, (0, 70, 80), left_paddle.inflate(8, 8))
            pygame.draw.rect(screen, (70, 25, 100), right_paddle.inflate(8, 8))

            pygame.draw.rect(screen, CYAN, left_paddle)
            pygame.draw.rect(screen, PURPLE, right_paddle)

            left_text = font.render(str(score_left), True, CYAN)
            right_text = font.render(str(score_right), True, PURPLE)

            screen.blit(left_text, (WIDTH // 4, 30))
            screen.blit(right_text, (3 * WIDTH // 4, 30))

            if game_over:
                if score_left >= 10:
                    message = "JOUEUR GAUCHE GAGNE!"
                else:
                    message = "JOUEUR DROIT GAGNE!"
                winner_text = menu_small_font.render(message, True, PURPLE)
                screen.blit(
                    winner_text,
                    (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2),
                )
                restart_text = menu_small_font.render(
                    "Appuyez sur R pour recommencer", True, (255, 220, 80)
                )
                screen.blit(
                    restart_text,
                    (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 45),
                )

            pygame.draw.circle(
                screen, (0, 70, 80), (int(ball_x), int(ball_y)), ball_radius + 4
            )
            pygame.draw.circle(screen, CYAN, (int(ball_x), int(ball_y)), ball_radius)

            pygame.draw.rect(screen, CYAN, left_paddle)
            pygame.draw.rect(screen, PURPLE, right_paddle)

            # Afficher les scores
            left_text = font.render(str(score_left), True, CYAN)
            right_text = font.render(str(score_right), True, PURPLE)

            screen.blit(left_text, (WIDTH // 4, 30))
            screen.blit(right_text, (3 * WIDTH // 4, 30))

            # Vérifier si un joueur a gagné
            if score_left >= 10 or score_right >= 10:
                game_over = True

            if game_over:
                if score_left >= 10:
                    winner_text = font.render("JOUEUR GAUCHE GAGNE!", True, CYAN)
                else:
                    winner_text = font.render("JOUEUR DROIT GAGNE!", True, PURPLE)
                    screen.blit(
                        winner_text,
                        (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2),
                    )

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Limiter le nombre de frames par seconde
    clock.tick(60)
pygame.quit()

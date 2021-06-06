import pygame
import sys
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

HEALTH_FONT = pygame.font.SysFont("bitstreamverasans", 20)
WINNER_FONT = pygame.font.SysFont("bitstreamverasans", 50)

FPS = 60
VEL = 3.5
BULLET_VEL = 7

MAX_BULLETS = 4

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# working with images
SPACESHIP_WID, SPACESHIP_HEI = (90, 50)

YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))

RED_SPACESHIP_IMG = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))

YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_WID, SPACESHIP_HEI)), 90)

RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WID, SPACESHIP_HEI)), 270)

SPACE_IMG = pygame.image.load(os.path.join("Assets", "space.png")).convert()

SPACE = pygame.transform.scale(SPACE_IMG, (WIDTH, HEIGHT))



def draw_window(yellow, red, yellow_bullets, red_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, (255, 255, 255), BORDER)

    yellow_health_text = HEALTH_FONT.render("Health : " + str(yellow_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health : " + str(red_health), 1, WHITE)

    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10 , 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def move_yellow(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 7:  # move left yellow
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # move right yellow
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 5:  # move up yellow
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:  # move down yellow
        yellow.y += VEL


def move_red(key_pressed, red):
    global VEL, BORDER
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # move left red
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH - 7:  # move right red
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 5:  # move up red
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # move down red
        red.y += VEL


def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x + BULLET_VEL >= WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))

            red_bullets.remove(bullet)

        elif bullet.x + BULLET_VEL <= 0:
            red_bullets.remove(bullet)


def show_winner(winner_text):
    display_text = WINNER_FONT.render(winner_text, 1, WHITE)

    WIN.blit(display_text, (WIDTH//2 - display_text.get_width() , HEIGHT//2 - display_text.get_height() ))
    pygame.display.update()
    pygame.time.delay(100)
    main()




def main():
    yellow = pygame.Rect(100, 100, SPACESHIP_HEI, SPACESHIP_WID)
    red = pygame.Rect(700, 100, SPACESHIP_HEI, SPACESHIP_WID)

    red_bullets = []
    yellow_bullets = []

    red_health = 3
    yellow_health = 3
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 7, 5)
                    yellow_bullets.append(bullet)
                    FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 7, 5)
                    red_bullets.append(bullet)
                    FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0 :
            winner_text = "Yellow won!"

        if yellow_health <= 0 :
            winner_text = "Red won!"

        if winner_text != "":
            show_winner(winner_text)

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_a] or key_pressed[pygame.K_s] or key_pressed[pygame.K_d] or \
                key_pressed[pygame.K_UP] or key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_LEFT] or key_pressed[
            pygame.K_RIGHT]:
            move_yellow(key_pressed, yellow)
            move_red(key_pressed, red)

        handle_bullets(red_bullets, yellow_bullets, red, yellow)
        draw_window(yellow, red, yellow_bullets=yellow_bullets, red_bullets=red_bullets,\
                    red_health=red_health, yellow_health=yellow_health)

    pygame.quit()


if __name__ == '__main__':
    main()

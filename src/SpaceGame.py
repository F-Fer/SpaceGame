import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!!")

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 62)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (220, 200, 0)
RED = (255, 0, 0)

BORDER = pygame.Rect(445, 0, 10, HEIGHT)

FPS = 60

VELOCITY = 5
BULLET_VEL = 7

MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))


def drawWin(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    yellow_health_text = HEALTH_FONT.render(("Health: " + str(yellow_health)), 1, YELLOW)
    red_health_text = HEALTH_FONT.render(("Health: " + str(red_health)), 1, RED)

    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x , yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    pygame.display.update()


def handle_yellow_movement(yellow, keys_pressed):
    if(keys_pressed[pygame.K_a] and (yellow.x - VELOCITY) > 0):                                   #left
        yellow.x -= VELOCITY
    if(keys_pressed[pygame.K_d] and (yellow.x + VELOCITY + SPACESHIP_HEIGHT) < BORDER.x):                                   #right
            yellow.x += VELOCITY
    if(keys_pressed[pygame.K_s] and (yellow.y + VELOCITY + SPACESHIP_WIDTH) < HEIGHT):                                   #down
        yellow.y += VELOCITY
    if(keys_pressed[pygame.K_w] and (yellow.y - VELOCITY) > 0):                                   #up
        yellow.y -= VELOCITY


def handle_red_movement(red, keys_pressed):
    if(keys_pressed[pygame.K_LEFT] and (red.x - VELOCITY) > (BORDER.x + 10)):                                #left
        red.x -= VELOCITY
    if(keys_pressed[pygame.K_RIGHT] and (red.x + VELOCITY + SPACESHIP_HEIGHT) < WIDTH):                               #right
        red.x += VELOCITY
    if(keys_pressed[pygame.K_DOWN] and (red.y + VELOCITY + SPACESHIP_WIDTH) < HEIGHT):                                #down
        red.y += VELOCITY
    if(keys_pressed[pygame.K_UP] and (red.y - VELOCITY) > 0):                                  #up
        red.y -= VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if(bullet.colliderect(red)):
            BULLET_HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif(bullet.x > WIDTH):
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if(bullet.colliderect(yellow)):
            BULLET_HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif(bullet.x < - 8):
            red_bullets.remove(bullet)


def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, ((WIDTH // 2) - (winner_text.get_width() // 2), (HEIGHT // 2) - 50))
    pygame.display.update()
    pygame.time.delay(2000)


def main():
    yellow = pygame.Rect(100, 100, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)      #(x, y, width, height)
    red = pygame.Rect(800, 100, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)         #(x, y, width, height)

    yellow_health = 5
    red_health = 5

    yellow_bullets = []
    red_bullets = []

    clock = pygame.time.Clock()

    run = True
    while(run):
        clock.tick(FPS)                                                 #makes shure game runs at 60 fps max
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
            
            if (event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LALT and len(yellow_bullets) < MAX_BULLETS):
                    bullet = pygame.Rect((yellow.x + SPACESHIP_HEIGHT), (yellow.y + SPACESHIP_WIDTH // 2 - 2), 8, 4)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE.play()
                if(event.key == pygame.K_RALT and len(red_bullets) < MAX_BULLETS):
                    bullet = pygame.Rect(red.x, (red.y + SPACESHIP_WIDTH // 2 - 2), 8, 4)
                    red_bullets.append(bullet)
                    BULLET_FIRE.play()
            if(event.type == YELLOW_HIT):
                yellow_health -= 1

            if(event.type == RED_HIT):
                red_health -= 1
            
        if(yellow_health <= 0):
            draw_winner("GAME OVER: RED WON!")
            yellow_health, red_health = 5 , 5
            red_bullets.clear()
            yellow_bullets.clear()
            

        
        if(red_health <= 0):
            draw_winner("GAME OVER: YELLOW WON!")
            yellow_health, red_health = 5, 5
            red_bullets.clear()
            yellow_bullets.clear()

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(yellow, keys_pressed)
        handle_red_movement(red, keys_pressed)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        drawWin(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)
    
    pygame.quit()

if( __name__ == "__main__"):                                            #makes shure game is only run when run directly
    main()      

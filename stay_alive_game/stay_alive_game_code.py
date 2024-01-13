import pygame    
import os   
import random

pygame.init()   
pygame.font.init() 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500  
FPS = 60

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
RESULT_FONT = pygame.font.SysFont('comicsans', 30)

PLAYER_DAMAGE = pygame.USEREVENT + 1
ADD_DIFFICULTY = pygame.USEREVENT + 2
ENEMY_DAMAGE = pygame.USEREVENT + 3
ADD_HEALTH = pygame.USEREVENT + 4
HEALTH_GAINED = pygame.USEREVENT + 5

PLAYER_WIDTH, PLAYER_HEIGHT = 70, 70
VEL = 8

MAX_BULLETS = 3
BULLET_VEL = 7

MAX_ENEMIES = 1
ENEMY_VEL = 5
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 40

LEVEL = 1
DIFFICULTY = 1

HEALTH_HEIGHT, HEALTH_WIDTH = 40, 40
MAX_HEALTH = 5

DIFFICULTY_TIMER = 5000
HEALTH_TIMER = 10000

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))   

#AHMA_IMAGE = pygame.image.load(os.path.join('ahma5.PNG')) 
ENEMY_IMAGE = pygame.image.load(os.path.join('enemy.PNG'))
PLAYER_IMAGE = pygame.image.load(os.path.join('player.PNG'))
HEALTH_IMAGE = pygame.image.load(os.path.join('health.PNG'))

#AHMA = pygame.transform.scale(AHMA_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))
PLAYER = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
HEALTH = pygame.transform.scale(HEALTH_IMAGE, (HEALTH_WIDTH, HEALTH_HEIGHT))

pygame.display.set_caption("Game :)")    



def draw_window(player, bullets, enemies, player_health, level, enemy_width, enemy_height, health_packets):
    SCREEN.fill(WHITE)
    SCREEN.blit(PLAYER, (player.x, player.y))

    for bullet in bullets:
        pygame.draw.rect(SCREEN, BLACK, bullet)

    for enemy in enemies:
        #pygame.draw.rect(SCREEN, RED, enemy)
        SCREEN.blit(pygame.transform.scale(ENEMY, (enemy_width, enemy_height)), (enemy.x, enemy.y))

    for health_pack in health_packets:
        #pygame.draw.rect(SCREEN, BLUE, health_pack)
        SCREEN.blit(HEALTH, (health_pack.x, health_pack.y))

    health_text = HEALTH_FONT.render("Health: " + str(player_health) + "    Level: " + str(level), 1, BLACK)

    SCREEN.blit(health_text, (SCREEN_WIDTH - health_text.get_width() - 10, 10))
    pygame.display.update()



def player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_LEFT] and player.x - VEL > 0:
        player.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and player.x + VEL < SCREEN_WIDTH - PLAYER_WIDTH:
        player.x += VEL

    if keys_pressed[pygame.K_UP] and player.y - VEL > 0:
        player.y -= VEL

    if keys_pressed[pygame.K_DOWN] and player.y + VEL < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player.y += VEL



def handle_bullets(bullets, player, enemies):
    for bullet in bullets:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            bullets.remove(bullet)
        for enemy in enemies:
            if enemy.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ENEMY_DAMAGE))
                enemies.remove(enemy)
                bullets.remove(bullet)



def handle_enemies(enemies, player, enemy_vel):
    for enemy in enemies:
        enemy.y += enemy_vel

        if player.colliderect(enemy):
            pygame.event.post(pygame.event.Event(PLAYER_DAMAGE))
            enemies.remove(enemy)

        elif enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)



def draw_result(text):
    draw_text = RESULT_FONT.render(text, 1, BLACK)
    SCREEN.blit(draw_text, (SCREEN_WIDTH // 2 - draw_text.get_width() // 2, SCREEN_HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


'''
def increase_difficulty():
    if DIFFICULTY <= 100:
        DIFFICULTY += 2
    if MAX_ENEMIES <= 100:
        MAX_ENEMIES += 1
    if ENEMY_WIDTH <= 50:
        ENEMY_WIDTH += 1
    if ENEMY_VEL <= 20:
        ENEMY_VEL += 1
    LEVEl += 1
'''

def handle_health_adding(health_packets, player):
    for health in health_packets:
        if player.colliderect(health):
            pygame.event.post(pygame.event.Event(HEALTH_GAINED))
            health_packets.remove(health)


def main():   

    player = pygame.Rect(SCREEN_WIDTH // 2, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    bullets = []
    enemies = []
    health_packets = []

    hits = 0
    text = ""
    player_health = MAX_HEALTH

    difficulty = DIFFICULTY
    max_enemies = MAX_ENEMIES
    enemy_width = ENEMY_WIDTH
    enemy_height = ENEMY_HEIGHT
    enemy_vel = ENEMY_VEL
    level = LEVEL

    done = False    
    clock = pygame.time.Clock()
    pygame.time.set_timer(ADD_DIFFICULTY, DIFFICULTY_TIMER)
    pygame.time.set_timer(ADD_HEALTH, HEALTH_TIMER)

    while not done:    
        clock.tick(FPS)
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:  
                done = True  
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player.x + PLAYER_WIDTH // 2 - 2, player.y - PLAYER_HEIGHT, 5, 10)
                    bullets.append(bullet)

            if event.type == PLAYER_DAMAGE:
                player_health -= 1

            if event.type == ENEMY_DAMAGE:
                hits += 1

            if event.type == ADD_DIFFICULTY:
                if difficulty <= 100:
                    difficulty += 5
                if max_enemies <= 100:
                    max_enemies += 1
                if enemy_width <= 100:
                    enemy_width += 5
                if enemy_height <= 100:
                    enemy_height += 5
                if enemy_vel <= 100:
                    enemy_vel += 1
                level += 1

            if event.type == ADD_HEALTH:
                health_pack = pygame.Rect(random.randrange(20, SCREEN_WIDTH - 20), random.randrange(20, SCREEN_HEIGHT - 20), HEALTH_WIDTH, HEALTH_HEIGHT)
                health_packets.append(health_pack)

            if event.type == HEALTH_GAINED:
                if player_health < MAX_HEALTH:
                    player_health += 1

        if player_health <= 0:
            text = "You lost :(  You got to level " + str(level) + "  and killed " + str(hits) + " enemies"

        

        if random.randrange(0, 100) < difficulty and len(enemies) < max_enemies:
            enemy = pygame.Rect(random.randrange(0, SCREEN_WIDTH), 0 - enemy_height, enemy_width, enemy_height)
            enemies.append(enemy)


        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, player)
        handle_enemies(enemies, player, enemy_vel)
        handle_bullets(bullets, player, enemies)
        handle_health_adding(health_packets, player)
        draw_window(player, bullets, enemies, player_health, level, enemy_width, enemy_height, health_packets)

        if text != "":
            draw_result(text)   
            break

    main()    


if __name__ == "__main__":
    main()
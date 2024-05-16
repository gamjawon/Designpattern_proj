import pygame
import random
import os
import sys
import time

# ----- 게임창 위치설정 -----

win_posx = 700
win_posy = 300
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_posx, win_posy)

# ----- 전역 -----

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
FPS = 60

score = 0
playtime = 1

# ----- 색상 -----

BLACK = 0, 0, 0
WHITE = 255,255,255
RED = 255, 0, 0
GREEN1 = 25, 102, 25
GREEN2 = 51, 204, 51
GREEN3 = 233, 249, 185
BLUE = 17, 17, 212
BLUE2 = 0, 0, 255
YELLOW = 255, 255, 0
LIGHT_PINK1 = 255, 230, 255
LIGHT_PINK2 = 255, 204, 255

def initialize_game(width, height):
    pygame.init()
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pygame Shmup")
    return surface

def game_loop(surface):
    clock = pygame.time.Clock()
    sprite_group = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = PlayerShip()
    global player_health
    player_health= 100
    global score
    score = 0
    sprite_group.add(player)
    for i in range(7):
        enemy = Mob()
        sprite_group.add(enemy)
        mobs.add(enemy)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE:
                    player.shoot(sprite_group, bullets)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(sprite_group, bullets)


        sprite_group.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            mob = Mob()
            sprite_group.add(mobs)
            mobs.add(mob)
            score += 10

        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            print('a mob hits player!')
            player_health -= 1
            if player_health < 0:
                gameover(surface)
                close_game()
                restart()

        surface.fill(LIGHT_PINK1)
        sprite_group.draw(surface)
        score_update(surface)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    print('game played: ',playtime)

def score_update(surface):
    font = pygame.font.SysFont('malgungothic',35)
    image = font.render(f'  점수 : {score}  HP: {player_health} ', True, BLUE2)
    pos = image.get_rect()
    pos.move_ip(20,20)
    pygame.draw.rect(image, BLACK,(pos.x-20, pos.y-20, pos.width, pos.height), 2)
    surface.blit(image, pos)

def gameover(surface):
    font = pygame.font.SysFont('malgungothic',50)
    image = font.render('GAME OVER', True, BLACK)
    pos = image.get_rect()
    pos.move_ip(50, int(SCREEN_HEIGHT/2))
    surface.blit(image, pos)
    pygame.display.update()
    time.sleep(2)

def close_game():
    pygame.quit()
    print('Game closed')

def restart():
    screen = initialize_game(SCREEN_WIDTH,SCREEN_HEIGHT)
    game_loop(screen)
    close_game()

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40,30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = int(SCREEN_WIDTH / 2)
        self.rect.centery = SCREEN_HEIGHT - 20
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -10
        if keystate[pygame.K_d]:
            self.speedx = 10
        if keystate[pygame.K_w]:
            self.speedy = -10
        if keystate[pygame.K_s]:
            self.speedy = 10
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self, all_sprites,bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,30))
        self.color = random.choice([BLACK, BLUE, RED, GREEN1, YELLOW])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.direction_change = False

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(GREEN1)
        self.rect = self.image.get_rect()
        self.rect.bottom = player_y
        self.rect.centerx = player_x
        self.speedy = - 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

if __name__ == '__main__':
    screen = initialize_game(SCREEN_WIDTH,SCREEN_HEIGHT)
    game_loop(screen)
    sys.exit()

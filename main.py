import pygame
import random
import os
import sys
import time

# —— 게임창 위치설정 ——

win_posx = 700
win_posy = 300
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_posx, win_posy)

# —— 전역 ——

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
FPS = 60

# —— 색상 ——

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN1 = 25, 102, 25
GREEN2 = 51, 204, 51
GREEN3 = 233, 249, 185
BLUE = 17, 17, 212
BLUE2 = 0, 0, 255
YELLOW = 255, 255, 0
LIGHT_PINK1 = 255, 230, 255
LIGHT_PINK2 = 255, 204, 255

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pygame Shmup")
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = PlayerShip(self)
        self.player_health = 100
        self.score = 0
        self.all_sprites.add(self.player)
        for i in range(7):
            mob = Mob(self)
            self.all_sprites.add(mob)
            self.mobs.add(mob)

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        print('Game played:', self.player_health)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.shoot()

    def update(self):
        self.all_sprites.update()
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            mob = Mob(self)
            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.score += 10
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
        if hits:
            print('A mob hits player!')
            self.player_health -= 1
            if self.player_health < 0:
                self.gameover()
                self.close_game()
                self.restart()

    def draw(self):
        self.screen.fill(LIGHT_PINK1)
        self.all_sprites.draw(self.screen)
        self.draw_text(f'점수: {self.score}  HP: {self.player_health}', 35, BLUE2, 20, 20)
        pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont('malgungothic', size)
        image = font.render(text, True, color)
        rect = image.get_rect()
        rect.topleft = (x, y)
        self.screen.blit(image, rect)

    def gameover(self):
        self.draw_text('GAME OVER', 50, BLACK, 50, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        time.sleep(2)

    def close_game(self):
        pygame.quit()
        print('Game closed')

    def restart(self):
        self.__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.run()

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.game)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 30))
        self.color = random.choice([BLACK, BLUE, RED, GREEN1, YELLOW])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((10, 20))
        self.image.fill(GREEN1)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

if __name__ == '__main__':
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.run()
    sys.exit()

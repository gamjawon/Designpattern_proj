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

SCREEN_WIDTH = 800    #700
SCREEN_HEIGHT = 600     #500
FPS = 60

EasyMode_speed=10  
HardMode_speed=5

EasyMode_Health=100
HardMode_Health=50
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







pygame.init()  #게임실행
gameDisplay=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #게임창 설정
pygame.display.set_caption("shoting game") 
clock=pygame.time.Clock() 
myFont = pygame.font.SysFont( "arial", 30, True, False) #텍스트에 사용할 폰트
title= myFont.render("Shooting game", True, BLACK) #화면에 띄워지는 제목 텍스트


class Button: #텍스트=이미지=버튼 (render함수를 통해 텍스트를 이미지화. 텍스트에 클릭 이벤트를 넣었으므로 버튼 취급)
    def __init__(self):        
        self.x=0 #텍스트의 기본 x좌표
        self.y=0 #텍스트의 기본 y좌표
        self.width=0 #텍스트의 가로길이
        self.height=0 #텍스트의 세로길이       
        self.x_act=0  #마우스를 텍스트 위에 올렸을 때의 텍스트 x좌표
        self.y_act=0 #마우스를 텍스트 위에 올렸을 때의 텍스트 y좌표
        self.action=None #클릭 시 수행되는 함수
        self.text1=None #=기본이미지(텍스트)
        self.text2=None #=마우스를 버튼 위에 올렸을 때의 이미지. text1과 text2는 색만 다름
        
    def click(self): #메소드 이름을 click이라 정했지만 마우스를 올렸을 때, 클릭할 때 기능 모두 포함
        mouse=pygame.mouse.get_pos() #마우스 좌표값 계산을 위한 변수
        click=pygame.mouse.get_pressed() #클릭 이벤트를 위한 변수
        if self.x+self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y : #마우스가 텍스트 위에 올라간 경우
            gameDisplay.blit(self.text2,(self.x_act,self.y_act)) #위에서 설정한 마우스가 텍스트 위에 올라갔을 때의 이벤트. 1:새 택스트 2.새로운 좌표
            if click[0] and self.action != None: #클릭 했을 때 함수실행
                time.sleep(1)
                self.action()
        else:  #마우스가 텍스트 위에 올라가 있지 않을 때의 좌표설정
            gameDisplay.blit(self.text1,(self.x,self.y))       


class Buttonbuilder:    #버튼빌더 (abstract)
    def set_x(self,x):
        pass
    def set_y(self,y):
        pass
    def set_width(self,width):
        pass
    def set_height(self,height):
        pass    
    def set_xact(self,x_act):
        pass
    def set_yact(self,y_act):
        pass
    def set_action(self,action=None):
        pass    
    def set_texts(self):
        pass

class HardButtonbuiler(Buttonbuilder): #하드난이도 버튼 빌더 (concrete)
    def __init__(self):
        self.button=Button()        
        self.game=Game(SCREEN_WIDTH, SCREEN_HEIGHT,HardMode_Health,HardMode_speed) #전역변수로 설정한 값들을 Game 인자로 전달
                                                                                   #SCREEN_WIDTH와 SCREEN_HEIGHT는 창 크기 변수. 나머지 둘은 난이도에 따른 변수
    def set_x(self, x):
        self.button.x=x
    def set_y(self, y):
        self.button.y=y
    def set_width(self,width): 
        self.button.width=width              
    def set_height(self,height):
        self.button.height=height    
    def set_xact(self,x_act):
        self.button.x_act=x_act
    def set_yact(self,y_act):
        self.button.y_act=y_act
    def set_action(self):
        self.button.action=self.game.run 
    def set_texts(self):
        self.button.text1=myFont.render("Hard", True, BLACK) #보여질 텍스트 설정
        self.button.text2=myFont.render("Hard", True, RED)
    def build(self):
        return self.button    

class EasyButtonbuiler(Buttonbuilder): #easy모드 버튼 빌더
    def __init__(self):
        self.button=Button()
        self.game=Game(SCREEN_WIDTH, SCREEN_HEIGHT,EasyMode_Health,EasyMode_speed) #easymode에 사용할 인자 전달
             
    def set_x(self, x):
        self.button.x=x
    def set_y(self, y):
        self.button.y=y
    def set_width(self,width): 
        self.button.width=width              
    def set_height(self,height):
        self.button.height=height    
    def set_xact(self,x_act):
        self.button.x_act=x_act
    def set_yact(self,y_act):
        self.button.y_act=y_act
    def set_action(self):
        self.button.action=self.game.run
    def set_texts(self):
        self.button.text1=myFont.render("Easy", True, BLACK) #보여질 텍스트 설정
        self.button.text2=myFont.render("Easy", True, RED)
    def build(self):
        return self.button        

class ButtonDirector:  #버튼을 생성할 Director
    def __init__(self,builder):
        self._builder=builder
    def construct(self,x,y,width,height,x_act,y_act):
          
        self._builder.set_x(x)
        self._builder.set_y(y)
        self._builder.set_width(width)
        self._builder.set_height(height)
        
        self._builder.set_xact(x_act)
        self._builder.set_yact(y_act)
        self._builder.set_action()
        self._builder.set_texts()
        return self._builder.build()
        


class Mainmenu():     #위의 모든 내용을 실행할 클래스
    def __init__(self): #버튼들 생성
        self.HB=HardButtonbuiler()
        self.EB=EasyButtonbuiler()
        self.director1=ButtonDirector(self.HB) 
        self.startButton=self.director1.construct(280,260,60,20,273,258)
        self.director2=ButtonDirector(self.EB)        
        self.quitButton=self.director2.construct(445,260,60,20,440,258)
       
    def mainmenu_running(self):           
    
        menu = True       
    
        while menu:
            for event in pygame.event.get(): #윈도우 창 끄면 게임 종료되는 코드
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            gameDisplay.fill(WHITE)        
        
        
            titletext = gameDisplay.blit(title,(220,150))
            self.startButton.click()
            self.quitButton.click()
            pygame.display.update()
            pygame.display.flip()
            clock.tick(15)
#------------------------------------------------------

class Game:
    def __init__(self, width, height, h, s): #h=health s=speed
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pygame Shmup")
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = PlayerShip(self,h,s)
        self.player_health = self.player.health
        #self.player_health = 100
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
                #self.restart()  #재시작 기능 제거

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

    def restart(self): #재시작 기능을 없애서 당장은 쓸모없는 메소드
        self.__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.run()

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, game,health,speed):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - 20
        self.speedx = 0
        self.speedy = 0
        
        self.health=health  #입력받은 체력
        self.updated_speed=speed #입력받은 스피드

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -self.updated_speed
        if keystate[pygame.K_d]:
            self.speedx = self.updated_speed
        if keystate[pygame.K_w]:
            self.speedy = -self.updated_speed
        if keystate[pygame.K_s]:
            self.speedy = self.updated_speed
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
    m=Mainmenu()
    m.mainmenu_running()    #메인메뉴를 실행하고 난이도 선택하면 자동으로 Game class의 run 메소드 실행
    sys.exit()

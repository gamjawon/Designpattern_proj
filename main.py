import pygame
import random
import os
import sys
import time


# —— 게임창 위치설정 ——

win_posx = 700import pygame
import random
import os
import sys
import time
from abc import ABC, abstractmethod



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

        self.background = pygame.image.load("Assets/space.png").convert() # 게임의 배경 이미지 load
        self.bg_rect = self.background.get_rect() 
        self.player_image = pygame.image.load('Assets/spaceship.png').convert() # 비행선 load
        self.bullet_image = pygame.image.load('Assets/shoot.png').convert()# bullet load
        

        # 게임을 실행하는데 있어 가장 많이 생성되는 객체는 Mob이다.
        # 이때 각각의 Mob이 그것의 이미지 파일을 가지고 있다면 게임을 실행할수록 메모리 사용량이 증가할 것이다.
        # 이를 방지하기 위해 flyweight pattern을 이용
        # static 변수인 이미지 파일을 공유시켜 Mob을 생성, Mob의 종류를 다양화 시키면서 데이터 사용량을 줄인다.
        self.enemy_image = [] # 적 비행선의 이미지를 넣을 리스트
        self.enemy_list = ['Assets/enemy_1.png', 'Assets/enemy_2.png', 'Assets/enemy_3.png', 'Assets/enemy_4.png', 'Assets/enemy_5.png', 'Assets/enemy_6.png', 'Assets/enemy_7.png', 'Assets/enemy_8.png']
        for img in self.enemy_list: # Mob의 이미지 파일을 load하여 리스트에 추가
            self.enemy_image.append(pygame.image.load(img).convert())

        self.shoot_sound = pygame.mixer.Sound('Assets/shoot.mp3') # bullet을 발사할 때 나는 소리
        self.shoot_sound.set_volume(0.1)
        self.explosion_sound = pygame.mixer.Sound('Assets/explosion.wav') # Mob이 죽을 때나는 소리
        self.explosion_sound.set_volume(0.1)

        pygame.mixer.music.load("Assets/Background.wav") 
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = PlayerShip(self,self.player_image,h,s) # player 생성시 이미지를 인자로 받는다.
        self.player_health = self.player.health
        #self.player_health = 100
        self.score = 0
        self.all_sprites.add(self.player)

        self.score_observer = ScoreObserver() # observer pattern 사용하여 코드 모듈화 + 유연하게 만듦. 
        # 추후 게임에 새로운 요소가 추가될 시 점수 관찰에 필요한 로직이 변경되지 않음. 
        # 코드 응집도가 높아지고 유지보수하기 쉬운 장점이 있다. 
        self.player.register_observer(self.score_observer)
        for i in range(7):
            mob = Mob(self.enemy_image)  # Mob 생성시 이미지를 인자로 받는다.
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
                    self.player.shoot(self.bullet_image, self.shoot_sound) # bullet 생성시 이미지를 인자로 받는다.
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.shoot(self.bullet_image, self.shoot_sound)

    def update(self):
        self.all_sprites.update()# sprite에 포함된 모든 객체에 대해 update
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            self.explosion_sound.play() # Mob이 격추되었을 때 폭발 음성 출력
            mob = Mob(self.enemy_image)
            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.score_observer.update('enemy_killed') # observer pattern 이용 
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
        self.screen.blit(self.background, self.bg_rect) # 배경 이미지 출력
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
        self.draw_text('GAME OVER', 50, WHITE, 50, SCREEN_HEIGHT // 2)
        self.draw_text(f'Score : {self.score}', 50, WHITE, 50, (SCREEN_HEIGHT // 2)+50) # gameover시 점수도 출력하도록 함
        pygame.display.flip()
        time.sleep(2)

    def close_game(self):
        pygame.quit()
        print('Game closed')

    def restart(self): #재시작 기능을 없애서 당장은 쓸모없는 메소드
        self.__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.run()

class Subject:
    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, event):
        for observer in self._observers:
            observer.update(event)
# scoreObserver class가 옵저버로 작동. Observer 추상 클래스를 구현하고 있고 update 메서드를 오버라이드하여 
# 게임 내에서 발생한 이벤트에 대한 처리를 정의.
class Observer(ABC):
    @abstractmethod
    def update(self, event):
        pass

class ScoreObserver(Observer):
    def __init__(self):
        self.score = 0

    def update(self, event):
        if event == 'enemy_killed':
            self.score += 10


class PlayerShip(pygame.sprite.Sprite, Subject):
    def __init__(self, game, image, health,speed):
        pygame.sprite.Sprite.__init__(self)
        Subject.__init__(self)  # Subject 클래스 초기화
        self.game = game
        self.image = pygame.transform.scale(image, (75, 40)) # 인자로 받은 이미지 크기 조정
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        # self.radius = int(self.rect.width * .9/2)
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - 20
        self.speedx = 0
        self.speedy = 0
        
        self.health=health  #입력받은 체력
        self.updated_speed=speed #입력받은 스피드

    def update(self):
        # ship 조종
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
        # 밖으로 나가지 않게 위치 조정
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
    
    def shoot(self, image, sound):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.game, image)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)
        sound.play() # 발사할 때 음성 출력
        self.notify_observers('bullet_fired')
    

class Mob(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        # 인자로 받은 이미지 리스트에서 이미지를 랜덤 적용
        self.image_origin = pygame.transform.rotozoom(random.choice(image), 0, 0.7) 

        self.image = self.image_origin
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # mob이 스크린을 벗어나면 위에서 다시생성
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, game, image):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(image, (40, 70))
        self.image.set_colorkey(BLACK)
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

        self.background = pygame.image.load('Assets\space.png').convert() # 게임의 배경 이미지 load
        self.bg_rect = self.background.get_rect() 
        self.player_image = pygame.image.load('Assets\spaceship.png').convert() # 비행선 load
        self.bullet_image = pygame.image.load('Assets\shoot.png').convert()# bullet load
        # 게임을 실행하는데 있어 가장 많이 생성되는 객체는 Mob이다.
        # 이때 각각의 Mob이 그것의 이미지 파일을 가지고 있다면 게임을 실행할수록 메모리 사용량이 증가할 것이다.
        # 이를 방지하기 위해 flyweight pattern을 이용
        # static 변수인 이미지 파일을 공유시켜 Mob을 생성, Mob의 종류를 다양화 시키면서 데이터 사용량을 줄인다.
        self.enemy_image = [] # 적 비행선의 이미지를 넣을 리스트
        self.enemy_list = ['Assets\enemy_1.png', 'Assets\enemy_2.png', 'Assets\enemy_3.png', 'Assets\enemy_4.png', 'Assets\enemy_5.png', 'Assets\enemy_6.png', 'Assets\enemy_7.png', 'Assets\enemy_8.png']
        for img in self.enemy_list: # Mob의 이미지 파일을 load하여 리스트에 추가
            self.enemy_image.append(pygame.image.load(img).convert())

        self.shoot_sound = pygame.mixer.Sound('Assets\shoot.mp3') # bullet을 발사할 때 나는 소리
        self.shoot_sound.set_volume(0.1)
        self.explosion_sound = pygame.mixer.Sound('Assets\explosion.wav') # Mob이 죽을 때나는 소리
        self.explosion_sound.set_volume(0.1)

        pygame.mixer.music.load("Assets\Background.wav") # 배경음
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)

        self.clock = pygame.time.Clock()
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = PlayerShip(self,self.player_image,h,s) # player 생성시 이미지를 인자로 받는다.
        self.player_health = self.player.health
        #self.player_health = 100
        self.score = 0
        self.all_sprites.add(self.player)
        for i in range(7):
            mob = Mob(self.enemy_image)  # Mob 생성시 이미지를 인자로 받는다.
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
                    self.player.shoot(self.bullet_image, self.shoot_sound) # bullet 생성시 이미지를 인자로 받는다.
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.shoot(self.bullet_image, self.shoot_sound)

    def update(self):
        self.all_sprites.update()# sprite에 포함된 모든 객체에 대해 update
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in hits:
            self.explosion_sound.play() # Mob이 격추되었을 때 폭발 음성 출력
            mob = Mob(self.enemy_image)
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
        self.screen.blit(self.background, self.bg_rect) # 배경 이미지 출력
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
        self.draw_text('GAME OVER', 50, WHITE, 50, SCREEN_HEIGHT // 2)
        self.draw_text(f'Score : {self.score}', 50, WHITE, 50, (SCREEN_HEIGHT // 2)+50) # gameover시 점수도 출력하도록 함
        pygame.display.flip()
        time.sleep(2)

    def close_game(self):
        pygame.quit()
        print('Game closed')

    def restart(self): #재시작 기능을 없애서 당장은 쓸모없는 메소드
        self.__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.run()

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, game, image, health,speed):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(image, (75, 40)) # 인자로 받은 이미지 크기 조정
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        # self.radius = int(self.rect.width * .9/2)
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - 20
        self.speedx = 0
        self.speedy = 0
        
        self.health=health  #입력받은 체력
        self.updated_speed=speed #입력받은 스피드

    def update(self):
        # ship 조종
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
        # 밖으로 나가지 않게 위치 조정
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
    
    def shoot(self, image, sound):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.game, image)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)
        sound.play() # 발사할 때 음성 출력
    

class Mob(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        # 인자로 받은 이미지 리스트에서 이미지를 랜덤 적용
        self.image_origin = pygame.transform.rotozoom(random.choice(image), 0, 0.7) 

        self.image = self.image_origin
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # mob이 스크린을 벗어나면 위에서 다시생성
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, game, image):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.transform.scale(image, (40, 70))
        self.image.set_colorkey(BLACK)
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

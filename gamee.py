import pygame
import random
from menu import *
from pygame import mixer


class Game:

    def __init__(self):
        pygame.init()  # Init pygame
        self.FPS = 60
        self.fpsClock = pygame.time.Clock()
        self.shootSpeed = 10
        self.xScreen, self.yScreen = 627, 705  # Screen create
        self.VBullet = 15  # Tốc độ Bullet
        self.VPlanes = 15  # Tốc độ Planes
        self.VEnemy = 6  # Tốc độ Enemy
        self.scores = 0  # Điểm số
        self.numberEnemy = 2  # Số lượng enemy trong một screen
        self.numberBullet = 6  # Số bullet trong một screen
        self.linkBackGround = './data/background 1.jpg'  # Đường dẫn ảnh background
        self.linkEnemy = './data/enemy.png'  # Đường dẫn ảnh Enemy
        self.linkPlanes = './data/planes.png'  # Đường dẫn ảnh Planes
        self.musicBullet = mixer.Sound('./data/laser.wav')
        self.musicBackground = mixer.Sound('./data/Victory.wav')
        
        self.musicTheme = mixer.Sound('./data/musictheme.wav')
        self.musicEnd = mixer.Sound('./data/musicend.mp3')
        self.sizexPlanes, self.sizeyPlanes = 80, 80
        self.xPlanes, self.yPlanes = self.xScreen / \
            2-50, self.yScreen  # Khởi tao vị trí ban đầu planes


    #phục vụ cho phần Menu
        self.display = pygame.Surface((self.xScreen,self.yScreen)) 
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.font_name = '8-BIT WONDER.TTF'
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu
        self.running, self.playing = True, True


    #phục vụ cho hiệu ứng khi bắn trúng enemy:
        #đường dẫn ảnh cho hiệu ứng nổ   
        
        #kích thước hiệu ứng nổ = size Enemy
        self.sizexExplode, self.sizeyExplode = self.xPlanes, self.yPlanes     
        self.musicDestroy=mixer.Sound('./data/destroy.wav')   #link hiệu ứng âm thanh khi nổ
        self.linkEffectDestroy = self.main_menu.chooseEffect
        
    #khởi tạo màn hình game
        self.screen = pygame.display.set_mode(
            (self.xScreen, self.yScreen))  # Khởi tao kích thước màn hình
        pygame.display.set_caption("Space Invaders")
        self.background = pygame.image.load(self.linkBackGround)
        icon = pygame.image.load(self.linkPlanes)
        pygame.display.set_icon(icon)  # Set icon cho screen
        self.gamerunning = True
        self.listBullet = []
        self.listEnemy = []
        self.YGameOver = 0
        self.K_DOWN = self.K_UP = self.K_LEFT = self.K_RIGHT = False

        self.linkBullet = self.main_menu.chooseBullet

    # Đường dẫn ảnh hiển thị khi thua
        self.gameOverLinkImg = './data/gameOver.png'

    # Đặt state cho musicBackground
        self.musicStatus = True
        

    def show_score(self, x, y, scores, size):  # Hiển thị điểm
        font = pygame.font.SysFont("comicsansms", size)
        score = font.render(str(scores), True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def image_draw(self, url, xLocal, yLocal, xImg, yImg):  # In ra ngoài hình ảnh
        PlanesImg = pygame.image.load(url)
        PlanesImg = pygame.transform.scale(
            PlanesImg, (xImg, yImg))  # change size image
        self.screen.blit(PlanesImg, (xLocal, yLocal))

    def enemy(self):  # Quản lý Enemy
        for count, i in enumerate(self.listEnemy):
            xEnemy = i["xEnemy"]  # Lấy toạn độ X
            yEnemy = i["yEnemy"]  # Lấy toạn độ Y
            if xEnemy < 0 or xEnemy > self.xScreen - self.sizexPlanes:  # Nếu chạm vào hai bên phải trái
                # thì đổi hướng
                self.listEnemy[count]["direction"] = not self.listEnemy[count]["direction"]
            self.image_draw(self.linkEnemy, xEnemy, yEnemy, self.sizexPlanes,
                            self.sizeyPlanes)  # In enemy ra màn hình
            self.listEnemy[count]["xEnemy"] = xEnemy + \
                (self.VEnemy if self.listEnemy[count]
                 ["direction"] == False else -self.VEnemy)
            self.listEnemy[count]["yEnemy"] = yEnemy + \
                self.VEnemy / 2.5  # Toạn độ x xông tốc độ Enemy/3
            # Gán giá trị lớn nhất của Enemy theo y
            self.YGameOver = yEnemy if yEnemy > self.YGameOver else self.YGameOver

    def bullet(self):
        for count, i in enumerate(self.listBullet):
            xBullet = i["xBullet"]  # Lấy trục tọa độ theo X
            yBullet = i["yBullet"]  # Lấy trục tọa độ theo X
            self.image_draw(
                self.linkBullet, xBullet+13,
                yBullet, 25, 60)  # In ra bullet
            self.listBullet[count]["yBullet"] = yBullet - \
                self.VBullet  # Tiến y vè phía trước
            if yBullet <= 5:  # nếu toạn độ Y phía trên nàm hình thì xóa
                self.listBullet.remove(self.listBullet[count])

    def run(self):
        
        print(self.curr_menu.state)
        print(self.linkEffectDestroy)
        i = 0
        while self.gamerunning:
            # tạo cuộn dọc(nền chuyển động)
            self.screen.blit(self.background, [0, i])
            self.screen.blit(self.background, [0, -self.yScreen + i])
            if i == self.yScreen:
                i = 0
            i += 1

            # xét điều kiện để phát nhạc (khi nút M được nhấn thì đổi trạng thái)
            if self.musicStatus == True: 
                mixer.Sound.play(self.musicBackground)
                pygame.mixer.unpause()
            else:
                pygame.mixer.pause()

            for event in pygame.event.get():  # Bắt các sự kiện
                if event.type == pygame.QUIT:  # sự kiện nhấn thoát
                    self.gamerunning = False
                if event.type == pygame.KEYDOWN:  # sự kiện có phím nhấn xuống
                    if event.key == pygame.K_DOWN:
                        self.K_DOWN = True
                    if event.key == pygame.K_UP:
                        self.K_UP = True
                    if event.key == pygame.K_LEFT:
                        self.K_LEFT = True
                    if event.key == pygame.K_RIGHT:
                        self.K_RIGHT = True
                    if event.key == pygame.K_SPACE:
                        mixer.Channel(0).play(mixer.Sound(self.musicBullet))
                        if len(self.listBullet) < self.numberBullet:
                            self.listBullet.append({  # Add Thêm bullet
                                "xBullet": self.xPlanes + self.sizexPlanes / 2 - 25,
                                "yBullet": self.yPlanes - self.sizexPlanes / 2,
                            })

                    # khi nhấn M thì đổi trạng thái của musicBackground
                    if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            if self.musicStatus:
                                self.musicStatus = False
                            else:
                                self.musicStatus= True

                if event.type == pygame.KEYUP:  # sự kiện thả phím
                    if event.key == pygame.K_DOWN:
                        self.K_DOWN = False
                    if event.key == pygame.K_UP:
                        self.K_UP = False
                    if event.key == pygame.K_LEFT:
                        self.K_LEFT = False
                    if event.key == pygame.K_RIGHT:
                        self.K_RIGHT = False

            if self.K_DOWN:
                self.yPlanes = self.yPlanes + self.VPlanes / 2  # Tiến lên
            if self.K_UP:
                self.yPlanes = self.yPlanes - self.VPlanes / 2  # Tiến xuống
            if self.K_LEFT:
                self.xPlanes = self.xPlanes - self.VPlanes  # Tiến trái
            if self.K_RIGHT:
                self.xPlanes = self.xPlanes + self.VPlanes  # Tiến phải

            # tat tieng
            

            # Kiểm tra có vượt quá giới hạn màn hình  và sát về lề màn hình
            self.xPlanes = 0 if self.xPlanes < 0 else self.xPlanes
            self.xPlanes = self.xScreen - self.sizexPlanes if self.xPlanes + \
                self.sizexPlanes > self.xScreen else self.xPlanes
            self.yPlanes = 0 if self.yPlanes < 0 else self.yPlanes
            self.yPlanes = self.yScreen - self.sizeyPlanes if self.yPlanes + \
                self.sizeyPlanes > self.yScreen else self.yPlanes

            # nếu số lượng Enemy ít hơn self.numberEnemy thì tạo thêm
            if len(self.listEnemy) < self.numberEnemy:
                self.listEnemy.append({
                    "xEnemy": random.randint(0, self.xScreen - self.sizexPlanes),
                    "yEnemy": random.randint(-50, int(self.yScreen / 8)),
                    "direction": random.choice((True, False))
                })
            listEnemy2 = self.listEnemy
            # Kiểm tra có trúng bullet
            for countEnemy, enemyIteam in enumerate(listEnemy2):
                xEnemy = enemyIteam["xEnemy"]
                yEnemy = enemyIteam["yEnemy"]
                for countBullet, bulletIteam in enumerate(self.listBullet):
                    xBullet = bulletIteam["xBullet"]
                    yBullet = bulletIteam["yBullet"]
                    # Kiểm tra bullet có nằm giữa Enemy theo trục x không
                    isInX = xEnemy <= xBullet <= xEnemy + self.sizexPlanes
                    # Kiểm tra bullet có nằm giữa Enemy theo trục y không
                    isInY = yEnemy <= yBullet <= yEnemy + self.sizexPlanes / 1.2
                    if isInX and isInY:  # nếu nằm giữa
                        self.listEnemy.remove(
                            self.listEnemy[countEnemy])  # Xóa Enemy
                        self.listBullet.remove(
                            self.listBullet[countBullet])  # Xóa Bullet
                        self.scores = self.scores + 1  # CỘng thêm điểm

                        mixer.Channel(0).play(mixer.Sound(self.musicDestroy)) #phát âm thanh destroy
                
                        self.image_draw(self.linkEffectDestroy, xEnemy, yEnemy, self.sizexPlanes, 
                            self.sizeyPlanes)  # In vụ nổ ra màn hình 

                        break
            if self.numberEnemy < 7:
                self.numberEnemy = (self.scores / 15) + 2
            if self.YGameOver > self.yScreen - 50:  # Nếu Enemy về gần đích
                newGame = False
                mixer.stop()
                self.musicEnd.play(1000000)
                while True:
                    for event in pygame.event.get():  # Nếu nhấn
                        if event.type == pygame.QUIT:  # Thoát
                            self.gamerunning = False
                            newGame = True
                            mixer.stop()
                            break
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Thoát
                            newGame = True
                            mixer.stop()
                            break
                    if newGame:  # Thoát vòng while để vào game mới
                        break
                    self.show_score(100, 100, "Scores:{}".format(
                        self.scores), 40)  # In điểm
                    # self.show_score(self.xScreen / 2 - 150, self.yScreen / 2 - 100,
                    #                 "GAME OVER", 50)  # In Thông báo thua
                    self.show_score(self.xScreen / 2 - 120, self.yScreen / 2+20,
                                    "Press Space to play again", 20)
                    self.image_draw(self.gameOverLinkImg,self.xScreen / 2 - 150,self.yScreen / 2-100,300,100)
                    pygame.display.update()
                    self.fpsClock.tick(self.FPS)
                self.scores = 0  # Trả các biến về giá trị ban đầu
                self.listBullet = []
                self.listEnemy = []
                self.YGameOver = 0
                self.xPlanes, self.yPlanes = self.xScreen / \
                    2 - 45, self.yScreen - 100  # Khởi tao vị trí ban đầu planes
                self.K_DOWN = self.K_UP = self.K_LEFT = self.K_RIGHT = False
            self.show_score(10, 10, "Scores:{}".format(self.scores), 35)
            self.show_score(self.xScreen - 100, 20, "Group 10", 15)
            self.enemy()
            self.bullet()
            self.image_draw(self.linkPlanes, self.xPlanes,
                            self.yPlanes, self.sizexPlanes, self.sizeyPlanes)
            pygame.display.update()  # Update
            self.fpsClock.tick(self.FPS)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gamerunning=False
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False


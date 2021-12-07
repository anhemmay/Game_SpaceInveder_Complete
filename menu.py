import pygame


class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.xScreen / 2, self.game.yScreen / 2 #tọa độ của dòng đầu tiên
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) # vẽ khối chữ nhật với kích thước 20*20 đựng dấu X
        self.offset = - 100    # định vị cho việc lùi dấu x sang trái 100 đơn vị

    def draw_cursor(self): # hàm vẽ dấu x (sẽ được gọi khi bấm phím lên/xuống)
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.screen.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "bullet1"
        self.bullet1x, self.bullet1y = self.mid_w, self.mid_h + 30
        self.bullet2x, self.bullet2y = self.mid_w, self.mid_h + 50
        self.bullet3x, self.bullet3y = self.mid_w, self.mid_h + 70
        self.bullet4x, self.bullet4y = self.mid_w, self.mid_h + 90
        self.bullet5x, self.bullet5y = self.mid_w, self.mid_h + 110

        self.chooseBullet = './data/bullet.png'
        self.chooseEffect = './data/explode 1.png'

        self.cursor_rect.midtop = (self.bullet1x + self.offset, self.bullet1y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(
                'Choose Bullet', 40, self.game.xScreen / 2, self.game.yScreen / 2 - 20)
            self.game.draw_text("Bullet 1", 20, self.bullet1x, self.bullet1y)
            self.game.draw_text("Bullet 2", 20, self.bullet2x, self.bullet2y)
            self.game.draw_text("Bullet 3", 20, self.bullet3x, self.bullet3y)
            self.game.draw_text("Bullet 4", 20, self.bullet4x, self.bullet4y)
            self.game.draw_text("Bullet 5", 20, self.bullet5x, self.bullet5y)
            self.game.draw_text("Press M to mute background music", 15, self.bullet5x, self.bullet5y+30)

            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'bullet1': 
                #nếu đang ở dòng bullet1 mà ấn phím xuống thì state sẽ chuyển sang dòng bullet2
                self.cursor_rect.midtop = (
                    self.bullet2x + self.offset, self.bullet2y)
                self.state = 'bullet2'
            elif self.state == 'bullet2':
                self.cursor_rect.midtop = (
                    self.bullet3x + self.offset, self.bullet3y)
                self.state = 'bullet3'
            elif self.state == 'bullet3':
                self.cursor_rect.midtop = (
                    self.bullet4x + self.offset, self.bullet4y)
                self.state = 'bullet4'
            elif self.state == 'bullet4':
                self.cursor_rect.midtop = (
                    self.bullet5x + self.offset, self.bullet5y)
                self.state = 'bullet5'
            elif self.state == 'bullet5':
                self.cursor_rect.midtop = (
                    self.bullet1x + self.offset, self.bullet1y)
                self.state = 'bullet1'

        elif self.game.UP_KEY:
            if self.state == 'bullet1':
                self.cursor_rect.midtop = (
                    self.bullet5x + self.offset, self.bullet5y)
                self.state = 'bullet5'
            elif self.state == 'bullet5':
                self.cursor_rect.midtop = (
                    self.bullet4x + self.offset, self.bullet4y)
                self.state = 'bullet4'
            elif self.state == 'bullet4':
                self.cursor_rect.midtop = (
                    self.bullet3x + self.offset, self.bullet3y)
                self.state = 'bullet3'
            elif self.state == 'bullet3':
                self.cursor_rect.midtop = (
                    self.bullet2x + self.offset, self.bullet2y)
                self.state = 'bullet2'
            elif self.state == 'bullet2':
                self.cursor_rect.midtop = (
                    self.bullet1x + self.offset, self.bullet1y)
                self.state = 'bullet1'


    def check_input(self): 
        self.move_cursor() 
        if self.game.START_KEY:
            self.game.gamerunning = True
            if self.state == 'bullet1': # tùy state để đặt bullet và hiệu ứng nổ 
                self.game.linkBullet = './data/bullet 1.png'
                self.game.linkEffectDestroy = './data/explode 1.png'
            elif self.state == 'bullet2':
                self.game.linkBullet = './data/bullet 2.png'
                self.game.linkEffectDestroy = './data/explode 7.png'
                
            elif self.state == 'bullet3':
                self.game.linkBullet = './data/bullet 3.png'
                self.game.linkEffectDestroy = './data/explode 6.png'

            elif self.state == 'bullet4':
                self.game.linkBullet = './data/bullet 4.png'
                self.game.linkEffectDestroy = './data/explode 3.png'

            elif self.state == 'bullet5':
                self.game.linkBullet = './data/bullet 5.png'
                self.game.linkEffectDestroy = './data/explode 4.png'

            self.run_display = False

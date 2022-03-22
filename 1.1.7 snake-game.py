import pygame as pg
from random import randrange as rr
from math import floor as fl

class Settings:
    def __init__(self):
        self.ver = '1.1.7'
        self.screen_height_width = 600, 600
        self.screen_x = self.screen_height_width[0]
        self.screen_y = self.screen_height_width[1]
        self.GREEN, self.RED, self.BLACK, self.WHITE = ((0, 255, 0), (255, 0, 0),
                                                        (0, 0, 0), (255, 255, 255))
        self.snake_color = self.GREEN
        self.color_apple_inside = 255, 100, 0
        self.square_size = 20
        self.lvl = 0
        self.fps_default = 10
        self.fps = self.fps_default
        self.step_fps = 0
        self.score = 0
        self.clock = pg.time.Clock()
        self.start, self.walls, self.rainbow = True, True, False
        self.fonts = [pg.font.SysFont("arial", 50), pg.font.SysFont("arial", 15)]
        self.start_snake = ((self.screen_x / 2) - self.square_size,
                            (self.screen_y / 2) - self.square_size)

    def start_menu(self, window):
        while True:
            self.clock.tick(self.fps_default)
            pg.display.set_caption(f'Snake {self.ver} Level: {settings.lvl}. Walls: {self.walls}, RGBSnake: {self.rainbow}.')
            window.blit(self.fonts[0].render("Press 'SPACE' to start.", 1, self.WHITE), (20, 10))
            window.blit(self.fonts[1].render(f"Use 'NUM+' or 'NUM-', for change level.", 1, self.WHITE), (20, 60))
            window.blit(self.fonts[1].render("Use 'TAB' for On or Off Walls", 1, self.WHITE), (20, 75))
            window.blit(self.fonts[1].render("Use 'R' for On or Off RGBSnake", 1, self.WHITE), (20, 90))
            window.blit(self.fonts[1].render(f"Your score: {self.score}, Snake speed:{round(settings.fps, 1)}.", 1, self.WHITE), (20, 105))
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return True
                    elif event.key == pg.K_TAB:
                        self.walls = not self.walls
                    elif event.key == pg.K_r:
                        self.rainbow = not self.rainbow
                    elif event.key == pg.K_KP_PLUS:
                        if self.lvl > -1 and self.lvl < 10:
                            self.lvl += 1
                            self.step_fps += 0.1
                    elif event.key == pg.K_KP_MINUS:
                        if self.lvl > 0 and self.lvl < 11:
                            self.lvl -= 1
                            self.step_fps -= 0.1
                    elif event.key == pg.K_SPACE:
                        return False


class Snake(Settings):
    def __init__(self, window):
        super().__init__()
        self.walls = settings.walls
        self.window = window
        self.next = True
        self.x, self.y = 0, 0
        self.head_snake = pg.draw.rect(self.window, settings.snake_color,
                                      [self.start_snake[0], self.start_snake[1],
                                       self.square_size-1, self.square_size-1],
                                        border_radius = 2)
        self.tails_pos = []
        self.apple_pos = []

    def add_tail(self, arg):
        self.apple_pos.append(arg)
        self.tail_snake = pg.draw.rect(self.window, self.color_apple_inside,
                                      [arg[0], arg[1], self.square_size-1, self.square_size-1],
                                       border_radius = 2)
        self.tails_pos.append([self.tail_snake.x, self.tail_snake.y])

    def snake_draw(self):
        if self.next == True:
            self.control()
            self.window.fill(self.BLACK)
            self.snake_tail = [self.head_snake.x, self.head_snake.y]
            self.head_snake.move_ip(self.x, self.y)
            if self.walls == True:
                if (self.head_snake.x < 0  or
                    self.head_snake.y < 0  or
                    self.head_snake.x >= self.screen_x or
                    self.head_snake.y >= self.screen_y):
                    self.x, self.y = 0, 0
                    self.next = False
            elif self.walls == False:
                if self.head_snake.x < 0:
                    self.head_snake.x = self.screen_x - self.square_size
                elif self.head_snake.y < 0:
                    self.head_snake.y = self.screen_y - self.square_size
                elif self.head_snake.x == self.screen_x:
                    self.head_snake.x = 0
                elif self.head_snake.y == self.screen_y:
                    self.head_snake.y = 0
            if settings.rainbow == True:
                settings.snake_color = (rr(1, 255), rr(1, 255), rr(1, 255))
            elif settings.rainbow == False:
                settings.snake_color = self.GREEN
            self.head_snake = pg.draw.rect(self.window, settings.snake_color,
                                        [self.head_snake.x, self.head_snake.y,
                                        self.square_size-1, self.square_size-1], border_radius = 2)
            for it, t in enumerate(self.tails_pos):
                self.snake_tail_exp = self.tails_pos[it]
                self.tails_pos[it] = self.snake_tail
                self.snake_tail = self.snake_tail_exp        
            for ia, apple in enumerate(self.apple_pos):
                if apple == self.snake_tail_exp:
                    self.apple_pos[ia] = self.snake_tail_exp
                if apple not in self.tails_pos:
                    self.apple_pos.pop(0)
            for s_xy in self.tails_pos:
                if settings.rainbow == True:
                    settings.snake_color = (rr(1, 255), rr(1, 255), rr(1, 255))
                elif settings.rainbow == False:
                    settings.snake_color = self.GREEN
                for a_xy in self.apple_pos:
                    if a_xy in self.tails_pos:
                            self.tail_snake = pg.draw.rect(self.window, self.color_apple_inside,
                                                        [a_xy[0], a_xy[1], self.square_size-1, self.square_size-1],
                                                        border_radius = 2)
                self.tail_snake = pg.draw.rect(self.window, settings.snake_color,
                                            [s_xy[0], s_xy[1], self.square_size-1, self.square_size-1],
                                            border_radius = 2)
                                
                    
                     
    def control(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings.start = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.next = False
                    return None
                elif event.key == pg.K_UP or event.key == pg.K_w:
                    if self.walls == True:
                        if self.head_snake.y > 0 - self.square_size and self.y == 0:
                            self.x, self.y = 0, -self.square_size  #  Up
                    elif self.walls == False:
                        if self.y == 0:
                            self.x, self.y = 0, -self.square_size  #  Up
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    if self.walls == True:
                        if self.head_snake.y <= self.screen_y and self.y == 0:
                            self.x, self.y = 0, self.square_size  #  Down
                    elif self.walls == False:
                        if self.y == 0:
                            self.x, self.y = 0, self.square_size  #  Down
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    if self.walls == True:
                        if self.head_snake.x > 0 - self.square_size and self.x == 0:
                            self.x, self.y = -self.square_size, 0  #  Left
                    elif self.walls == False:
                        if self.x == 0:
                            self.x, self.y = -self.square_size, 0  #  Left
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    if self.walls == True:
                        if self.head_snake.x <= self.screen_x and self.x == 0:
                            self.x, self.y = self.square_size, 0  #  Right
                    elif self.walls == False:
                        if self.x == 0:
                            self.x, self.y = self.square_size, 0  #  Right
        self.next = True

    def head_pos(self):
        return [self.head_snake.x, self.head_snake.y]


class Apple(Settings):
    def __init__(self):
        super().__init__()
        self.rand = [rr(0, self.screen_x, self.square_size),
                    rr(0, self.screen_y, self.square_size)]
        
    def new_apple(self, window):
        self.apple_new = pg.draw.rect(window, self.RED, 
                [self.rand[0], self.rand[1], self.square_size-1, self.square_size-1], border_radius = 5)
    
    def apple_pos(self):
        return [self.apple_new.x, self.apple_new.y]


if __name__ == '__main__':
    pg.init()
    settings = Settings()
    window = pg.display.set_mode(settings.screen_height_width)
    apple = Apple()
    snake = Snake(window)
    menu = settings.start_menu(window)
    if menu == False:
        settings.start = True
        snake = Snake(window)
    elif menu == True:
        settings.start = False
    while settings.start:
        pg.display.set_caption(f'Score: {settings.score} Level: {settings.lvl}. Snake speed:{round(settings.fps, 1)}. Walls: {settings.walls}')
        snake.snake_draw()
        apple.new_apple(window)
        for check in snake.tails_pos:
            if check == apple.apple_pos():
                apple = Apple()
                apple.new_apple(window)
            if check == snake.head_pos():
                snake.next = False
        if apple.apple_pos() == snake.head_pos():
            snake.add_tail(apple.apple_pos())
            apple = Apple()
            apple.new_apple(window)
            settings.score += 1
            settings.fps += settings.step_fps
            if settings.lvl == 0:
                if settings.score % 5 == 0:
                    settings.fps += 2
        if snake.next == False:
            menu = settings.start_menu(window)
            if menu == False:
                snake = Snake(window)
                snake.next = True
                settings.score = 0
                settings.fps = settings.fps_default
            elif menu == True:
                settings.start = False
        pg.display.update()
        settings.clock.tick(fl(settings.fps))

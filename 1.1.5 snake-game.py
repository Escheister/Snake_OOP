import pygame as pg
from random import randrange as rr

class InitPlayZone:
    def __init__(self):
        self.screen_height_width = 600, 600
        self.screen_x = self.screen_height_width[0]
        self.screen_y = self.screen_height_width[1]
        self.GREEN = 0, 255, 0
        self.RED = 255, 0, 0
        self.BLACK = 0, 0, 0
        self.WHITE = 255, 255, 255
        self.square_size = 20
        self.level = 0
        self.fps_default = 10
        self.fps = self.fps_default
        self.step_fps = 0
        self.score = 0
        self.clock = pg.time.Clock()
        self.start = True
        self.walls = True
        self.fonts = [pg.font.SysFont("arial", 50), pg.font.SysFont("arial", 15)]
        self.start_snake = ((self.screen_x / 2) - self.square_size,
                            (self.screen_y / 2) - self.square_size)

    def start_menu(self, window):
        while True:
            if self.walls == True:
                pg.display.set_caption(f'Snake. Your score: {settings.score}. Level: {settings.level}. Snake speed: {settings.fps}. Walls ON')
            elif self.walls == False:
                pg.display.set_caption(f'Snake. Your score: {settings.score}. Level: {settings.level}. Snake speed: {settings.fps}. Walls OFF')
            window.blit(self.fonts[0].render("Press 'R' to start.", 1, self.WHITE), (20, 10))
            window.blit(self.fonts[1].render(f'Your score: {self.score}!', 1, self.WHITE), (20, 60))
            window.blit(self.fonts[1].render(f'Use NUM+ or NUM-, for change your level.', 1, self.WHITE), (20, 75))
            window.blit(self.fonts[1].render('Use Enter for On or Off walls', 1, self.WHITE), (20, 90))
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return True, self.walls
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return True, self.walls
                    elif event.key == pg.K_KP_ENTER:
                        self.walls = not self.walls
                    elif event.key == pg.K_KP_PLUS:
                        if self.level > -1 and self.level < 10:
                            self.level += 1
                            self.step_fps += 0.1
                    elif event.key == pg.K_KP_MINUS:
                        if self.level > 0 and self.level < 11:
                            self.level -= 1
                            self.step_fps -= 0.1
                    elif event.key == pg.K_r:
                        return False, self.walls


class Snake(InitPlayZone):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.next = True
        self.x, self.y = 0, 0
        self.head_snake = pg.draw.rect(self.window, self.GREEN,
                                      [self.start_snake[0], self.start_snake[1],
                                       self.square_size, self.square_size])
        self.tails_pos = []

    def add_tail(self, arg):
        self.tail_snake = pg.draw.rect(self.window, self.GREEN,
                                      [arg[0], arg[1], self.square_size, self.square_size])
        self.tails_pos.append([self.tail_snake.x, self.tail_snake.y])

    def snake_draw(self, walls):
        if self.next == True:
            self.control(walls)
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
            self.head_snake = pg.draw.rect(self.window, self.GREEN,
                                        [self.head_snake.x, self.head_snake.y,
                                        self.square_size, self.square_size])
            for i, t in enumerate(self.tails_pos):
                self.snake_tail_exp = self.tails_pos[i]
                self.tails_pos[i] = self.snake_tail
                self.snake_tail = self.snake_tail_exp
            for s_xy in self.tails_pos:
                self.tail_snake = pg.draw.rect(self.window, self.GREEN,
                                            [s_xy[0], s_xy[1], self.square_size, self.square_size])

        
    def control(self, walls):
        self.walls = walls
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.start = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.start = False
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
        self.window.fill(self.BLACK)

    def head_pos(self):
        return [self.head_snake.x, self.head_snake.y]


class Apple(InitPlayZone):
    def __init__(self):
        super().__init__()
        self.rand = [rr(0, self.screen_x, self.square_size),
                    rr(0, self.screen_y, self.square_size)]
        
    def new_apple(self, window):
        self.apple_new = pg.draw.rect(window, self.RED, 
                [self.rand[0], self.rand[1], self.square_size, self.square_size])
    
    def apple_pos(self):
        return [self.apple_new.x, self.apple_new.y]


if __name__ == '__main__':
    pg.init()
    settings = InitPlayZone()
    window = pg.display.set_mode(settings.screen_height_width)
    snake = Snake(window)
    apple = Apple()
    menu, walls = settings.start_menu(window)
    if menu == False:
        snake.start = True
    elif menu == True:
        snake.start = False
    while snake.start:
        if walls == True:
            pg.display.set_caption(f'Snake. Your score: {settings.score}. Level: {settings.level}. Snake speed: {settings.fps}. Walls ON')
        elif walls == False:
            pg.display.set_caption(f'Snake. Your score: {settings.score}. Level: {settings.level}. Snake speed: {settings.fps}. Walls OFF')
        snake.snake_draw(walls)
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
            if settings.level == 0:
                if settings.score % 5 == 0:
                    settings.fps += 2
        if snake.next == False:
            menu, walls = settings.start_menu(window)
            if menu == False:
                snake = Snake(window)
                snake.next = True
                settings.score = 0
                settings.fps = settings.fps_default
            elif menu == True:
                snake.start = False
        pg.display.update()
        settings.clock.tick(settings.fps)
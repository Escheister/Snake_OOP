import pygame as pg
from random import randrange as rd


class Snake:
    def __init__(self, field_size=20, color=(0,255,0), display=None, display_size=(600,600)):
        self.field_size = field_size
        self.x, self.y = display_size
        self.pos_x, self.pos_y = ((self.x//2)-field_size, (self.y//2)-field_size)
        self.color = color
        self.display = display

    def head_snake(self):
        self.new_snake = pg.draw.rect(self.display, self.color, 
                    [self.pos_x, self.pos_y, self.field_size, self.field_size])
        self.tail_list = []
    
    def pos_head(self):
        return self.new_snake.x, self.new_snake.y

    def tail_snake(self, snake_pos_x, snake_pos_y):
        self.snake_tail = pg.draw.rect(self.display, self.color, 
                        [snake_pos_x, snake_pos_y, self.field_size, self.field_size])
        self.tail_list.append([self.snake_tail.x, self.snake_tail.y])

    def pos_tails(self):
        return self.tail_list

    def control_snake(self, x, y):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False, 0, 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False, 0, 0
                elif event.key == pg.K_UP or event.key == pg.K_w:
                    if self.new_snake.y > 0 - self.field_size and y == 0:
                        x, y = 0, -self.field_size  #  Up
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    if self.new_snake.y < self.y-self.field_size and y == 0:
                        x, y = 0, self.field_size  #  Down
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    if self.new_snake.x > 0 - self.field_size and x == 0:
                        x, y = -self.field_size, 0  #  Left
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    if self.new_snake.x < self.x-self.field_size and x == 0:
                        x, y = self.field_size, 0  #  Right

        if (self.new_snake.x < 0  or
            self.new_snake.y < 0  or
            self.new_snake.x >= self.x-self.field_size or
            self.new_snake.y >= self.y-self.field_size):
            x, y = 0, 0
            return False, 0, 0    
        self.display.fill((0,0,0))
        snake_x = self.new_snake.x
        snake_y = self.new_snake.y
        self.new_snake.move_ip(x, y)
        self.new_snake = pg.draw.rect(self.display, self.color, 
                    [self.new_snake.x, self.new_snake.y, self.field_size, self.field_size])
        for i, t in enumerate(self.tail_list):
            tail_x = self.tail_list[i][0]
            tail_y = self.tail_list[i][1]
            self.tail_list[i][0] = snake_x
            self.tail_list[i][1] = snake_y
            snake_x = tail_x
            snake_y = tail_y
        for t in self.tail_list:
            self.snake_tail = pg.draw.rect(self.display, self.color, 
                        [t[0], t[1], self.field_size, self.field_size]) 
        return True, x, y

    def end_game(self, font1, font2, color):
        while True:
            self.display.blit(font1.render("Press 'R' to restart.", 1, color), (20, 10))
            self.display.blit(font2.render(f'Your score: {count}', 1, color), (20, 60))
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        return False
                    elif event.key == pg.K_ESCAPE:
                        return True


class Apple:
    def __init__(self, field_size=20, color=(255, 0, 0), display=None, display_size=(600, 600), sp=(0,0)):
        self.field_size = field_size
        self.sp = sp
        self.display_size = display_size
        self.pos = (rd(0, self.display_size[0], self.field_size),
                    rd(0, self.display_size[1], self.field_size))
        if self.pos == self.sp:
            self.pos = (rd(0, self.display_size[0], self.field_size),
                        rd(0, self.display_size[1], self.field_size))
        self.color = color
        self.display = display

    def pos_new_apple(self):
        new_apple = pg.draw.rect(self.display, self.color, 
                    [self.pos[0], self.pos[1], self.field_size, self.field_size])
        return new_apple.x, new_apple.y
    
    def pos_apple(self, x, y):
        pg.draw.rect(self.display, self.color, 
                [x, y, self.field_size, self.field_size])
        

if __name__ == '__main__':
    fps_init = 10
    pg.init()
    font1 = pg.font.SysFont('arial', 50)
    font2 = pg.font.SysFont('arial', 25)
    START = True
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    screen_size = 600, 600
    window = pg.display.set_mode(screen_size)
    fps = fps_init
    field_size = 20
    snake = Snake(display=window, field_size=field_size, display_size=screen_size)
    snake.head_snake()
    snake_pos = snake.pos_head()
    apple = Apple(display=window, field_size=field_size, display_size=screen_size, sp=snake_pos)
    pg.display.update()
    clock = pg.time.Clock()
    x, y = 0, 0
    count = 0
    while START:
        pg.display.set_caption(f'Snake. Your score: {count}')
        pos_for_apple = snake.pos_tails()
        start, x, y = snake.control_snake(x, y)
        snake_pos = snake.pos_head()
        apple_pos = apple.pos_new_apple()
        apple.pos_apple(apple_pos[0], apple_pos[1])
        for t in snake.pos_tails():
            if t == list(snake_pos):
                start = False
            if t == list(apple_pos):
                apple = Apple(display=window, field_size=field_size, display_size=screen_size, sp=snake_pos)
        if apple_pos == snake_pos:
            apple = Apple(display=window, field_size=field_size, display_size=screen_size, sp=snake_pos)
            count += 1
            snake.tail_snake(apple_pos[0], apple_pos[1])
            fps += 1
        if start == False:
            end = snake.end_game(font1, font2, WHITE)
            if end == True:
                START = False
            else:
                START = True
                x, y = 0, 0
                fps = fps_init
                count = 0
                snake = Snake(display=window, field_size=field_size, display_size=screen_size)
                snake.head_snake()
                snake_pos = snake.pos_head()
                apple = Apple(display=window, field_size=field_size, display_size=screen_size, sp=snake_pos)          
        pg.display.update()
        clock.tick(fps)
    pg.display.quit()
    pg.quit()
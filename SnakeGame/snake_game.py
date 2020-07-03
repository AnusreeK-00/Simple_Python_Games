import pygame as pg
import random
import time


sw = 400
red = pg.Color(255, 0, 0)
green = pg.Color(0, 255, 0)
black = pg.Color(0, 0, 0)
white = pg.Color(255, 255, 255)
brown = pg.Color(165, 42, 42)

pg.init()

win = pg.display.set_mode((sw, sw))
pg.display.set_caption("Snake Game")

class Food():
    def __init__(self):
        self.x = sw/2
        self.y = sw/4
        self.color = red
        self.width = 10
        self.height = 10

    def draw_food(self, surface):
        self.food = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, self.color, self.food)


    #checks if head collided with food to determine if the food is eaten
    def is_eaten(self,head):
        return self.food.colliderect(head)

    #new pos for food
    def new_pos(self):
        self.x = random.randint(0, sw-self.width)
        self.y = random.randint(0,sw-self.height)



class Snake():
    def __init__(self):
        self.x = sw/2
        self.y = sw/2
        self.width = 10
        self.height = 10
        self.velocity = 10
        self.direction = 'stop'
        self.body = []
        self.head_color = green
        self.body_color = brown

    #draw snake
    def draw_snake(self, surface):
        self.seg = []
        self.head = pg.Rect(self.x, self.y, self.width, self.height)
        pg.draw.rect(surface, self.head_color, self.head)
        if len(self.body) > 0:
            for unit in self.body:
                segment = pg.Rect(unit[0], unit[1], self.width, self.height)
                pg.draw.rect(surface, self.body_color, segment)
                self.seg.append(segment)


    #Increase snake length
    def add_unit(self):
        if len(self.body) != 0:
            ind = len(self.body) - 1
            x = self.body[ind][0]
            y = self.body[ind][1]
            self.body.append([x,y])
        else:
            self.body.append([1000, 1000])

    #Collision check
    def is_collision(self):
        #Collision with itself
        for segment in self.seg:
            if self.head.colliderect(segment):
                return True

        #Collision with boundaries
        if self.y < 0 or self.y > sw-self.height or self.x < 0 or self.x > sw-self.width:
            return  True

    #Move the snake
    def move(self):
        for i in range(len(self.body)-1, 0, -1):
            x = self.body[i-1][0]
            y = self.body[i-1][1]
            self.body[i] = [x,y]

        if len(self.body) > 0:
            self.body[0] = [self.x, self.y]

        if self.direction == 'up':
            self.y -= self.velocity

        if self.direction == 'down':
            self.y += self.velocity

        if self.direction == 'left':
            self.x -= self.velocity

        if self.direction == 'right':
            self.x += self.velocity

    #Change direction of head
    def change_direction(self, direction):
        if self.direction != 'down' and direction == 'up':
            self.direction = 'up'
        if self.direction != 'up' and direction == 'down':
            self.direction = 'down'
        if self.direction != 'right' and direction == 'left':
            self.direction = 'left'
        if self.direction != 'left' and direction == 'right':
            self.direction = 'right'



score = 0
highscore = 0
#draw score
def draw_score(surface):
    global highscore
    font_name = pg.font.match_font('arial')
    if score > highscore:
        highscore = score

    # write score on screen
    font = pg.font.Font(font_name, 18)
    text_surface = font.render('Score: {} HighScore: {}'.format(score, highscore), True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (200,10)
    surface.blit(text_surface, text_rect)

#Game over
def game_over():
    global  score
    gameOverFont = pg.font.Font('freesansbold.ttf', 24)
    gameOverSurf = gameOverFont.render('Game Over', True, white)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (200,50)
    win.blit(gameOverSurf, gameOverRect)
    #reset score
    score = 0
    pg.display.flip()
    time.sleep(2)
    # re-initialize game
    run = True
    fd = Food()
    s = Snake()
    play_game(fd, s)



clock = pg.time.Clock()
def play_game(fd, s):
    global score
    run = True
    while run:
        clock.tick(10)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        win.fill(black)
        fd.draw_food(win)
        s.draw_snake(win)
        draw_score(win)

        #input
        pressed = pg.key.get_pressed()
        if pressed[pg.K_UP]:
            s.change_direction('up')
        if pressed[pg.K_DOWN]:
            s.change_direction('down')
        if pressed[pg.K_LEFT]:
            s.change_direction('left')
        if pressed[pg.K_RIGHT]:
            s.change_direction('right')

        #Move snake
        s.move()
        #Eat
        if fd.is_eaten(s.head):
            fd.new_pos()
            s.add_unit()
            score += 10
        #collision
        if s.is_collision():
            run = False
            game_over()

        pg.display.update()

fd = Food()
s = Snake()
play_game(fd, s)

pg.quit()
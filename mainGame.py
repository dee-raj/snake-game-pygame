import random
from time import sleep
import pygame
from pygame.locals import *

size = 32
class MyException(Exception):
    pass

class HomeCity:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.city = pygame.image.load("resources/snakeblock.png").convert()
        self.x = size * 3
        self.y = size * 3

    def draw(self):
        self.parent_screen.blit(self.city, (self.x, self.y))

    def move(self):
        self.x = random.randint(0, 31) * size
        self.y = random.randint(0, 15) * size


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/sblock.png").convert()
        pygame.mixer.init()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = 'down'

    def increse_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((111, 111, 5))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'up':
            self.y[0] -= size
        elif self.direction == 'down':
            self.y[0] += size
        elif self.direction == 'right':
            self.x[0] += size
        elif self.direction == 'left':
            self.x[0] -= size
        self.draw()


def playSound(filename):
    sound = pygame.mixer.Sound(f'resources/{filename}')
    pygame.mixer.Sound.play(sound)


def isCollition(x1, y1, x2, y2):
    if x1 <= x2 < x1 + size:
        if y1 <= y2 < y1 + size:
            return True
    return False


def bgMusic():
    pygame.mixer.music.load('resources/bg_music.mp3')
    pygame.mixer.music.play(100)
    pygame.mixer.music.set_volume(0.1)


class MyGame:
    def __init__(self):
        pygame.init()
        bgMusic()
        self.width = 1024
        self.height = 512
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.surface.fill((111, 111, 5))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.city = HomeCity(self.surface)
        self.gameOver = False

    def play(self):
        self.snake.walk()
        self.city.draw()
        # snake collide with apple/city
        if isCollition(self.snake.x[0], self.snake.y[0], self.city.x, self.city.y):
            self.snake.increse_length()
            self.city.move()
            playSound('tring.wav')

        # snake collide with itself
        for i in range(1, self.snake.length):
            if isCollition(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.gameOver = True
                raise MyException("Game End due to self collide")

        # frame boundary collition
        # left right
        if self.snake.x[0] + size > self.width or self.snake.x[0] < 0:
            self.gameOver = True
            raise MyException("Game End due to collide at left/right part")

        # top buttom 
        if self.snake.y[0] + size > self.height or self.snake.y[0] < 0:
            self.gameOver = True
            raise MyException("Game End due to collide at top/buttom part")

    def show_game_over(self):
        self.gameOver = True
        self.surface.fill((111, 111, 5))
        font = pygame.font.SysFont('arial', 40)
        gameOver = font.render(f"Game is Over! Your Score: {self.snake.length}", True, (255, 10, 1))
        self.surface.blit(gameOver, (100, 170))
        playAgain = font.render(f"Enter Return To Play Again", True, (255, 255, 255))
        self.surface.blit(playAgain, (100, 220))

    def display_Score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def RunGame(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        self.gameOver = True
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_SPACE:
                        pygame.mixer.music.pause()
                        pause = True

                    if event.key == K_p and not self.gameOver:
                        pause = False
                        pygame.mixer.music.unpause()

                    if event.key == K_RETURN and pause:
                        pause = False
                        self.gameOver = False
                        self.snake.x = [size] * self.snake.length
                        self.snake.y = [size] * self.snake.length
                        self.snake.direction = 'down'
                        self.snake.length = 1
                        pygame.mixer.music.unpause()

                    self.snake.draw()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
                    self.display_Score()
            except MyException as board:
                print(board)
                playSound('boom.wav')
                self.show_game_over()
                pause = True
                pygame.mixer.music.pause()
            pygame.display.flip()
            sleep(0.3)


if __name__ == "__main__":
    mg = MyGame()
    mg.RunGame()

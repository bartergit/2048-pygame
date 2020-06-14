from pygame import *
import sys
from itself2048 import Game



class DrawGame:  # Создаем игровой объект
    def __init__(self):
        font.init()
        self.width = 100
        self.padding = 10
        self.font = font.SysFont(None, 36)
        self.screen = display.set_mode((450,550))  # Создаем окно разрешением 640х480
        display.set_caption('2048')
        self.game = Game()
        self.rect = Rect(0, 100, self.width, self.width)
        self.anim = []
        self.clock = time.Clock()

    def animate_move(self, direction):
        self.game.move(direction)
        print(self.game)
        # time.set_timer(USEREVENT + 1, 30)
        # self.set_move(self.rect, (0,2))


    def move(self, event):
        if event.key == K_UP:
            self.animate_move("up")
        if event.key == K_DOWN:
            self.animate_move("down")
        if event.key == K_LEFT:
            self.animate_move("left")
        if event.key == K_RIGHT:
            self.animate_move("right")

    def start(self):
        while 1:
            for i in event.get():  
                if i.type == QUIT:
                    sys.exit()
                if i.type == KEYDOWN:
                    self.move(i)
            self.redraw()
            self.redraw()
            display.flip()
            self.clock.tick(30)
            self.screen.fill((255, 255, 255))

    def set_move(self, rect, direction):
        self.anim = [Rect(direction[0] * self.width, direction[1] * self.width, 0, 0), 0]


    def animate(self):
        if len(self.anim):
            t = self.anim[1]
            self.anim[1] += 1
            duration = 1000/30
            if self.anim[1] < duration:
                draw.rect(self.screen, (255,0,0), Rect(self.rect.x + self.anim[0].x * t / duration, self.rect.y + self.anim[0].y * t / duration, self.width, self.width))

    def redraw(self):
        tiles = [(i,j) for i in range(4) for j in range(4) if self.game.field[i][j] != 0]
        for i,j in tiles:
            tile_rect = draw.rect(self.screen, (255,0,0), Rect(j * (self.width + self.padding), i * (self.width + self.padding), self.width, self.width))
            text = self.font.render(str(self.game.field[i][j]), True, (0,0,0))
            txt_surface = self.font.render(str(self.game.field[i][j]), True, (255,255,255))
            text_rect = txt_surface.get_rect()
            self.screen.blit(txt_surface, [tile_rect.centerx - text_rect.width/2, tile_rect.centery - text_rect.height/2])




if __name__ == "__main__":
    Rect(3,5, 1, 0)
    drawGame = DrawGame()
    print(drawGame.game)
    drawGame.start()
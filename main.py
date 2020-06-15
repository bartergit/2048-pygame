from pygame import *
import sys
from itself2048 import Game
import yaml



class DrawGame:  # Создаем игровой объект
    WIDTH = 450
    HEIGHT = 550
    def __init__(self):
        font.init()
        self.width = 100
        self.padding = 10
        self.margin = 100
        self.font = font.SysFont(None, 50)
        self.screen = display.set_mode((DrawGame.WIDTH, DrawGame.HEIGHT))  # Создаем окно разрешением 640х480
        display.set_caption('2048')
        self.game = Game()
        self.rect = Rect(0, 100, self.width, self.width)
        self.anim = []
        self.clock = time.Clock()
        self.difference_list = []
        self.frame_counter = 0
        with open(r'colors.yaml') as file:
            self.colors = yaml.load(file, Loader=yaml.FullLoader)

    def get_color(self, key):
        color = self.colors.get(key, self.colors[4096])
        return color["Red"], color["Green"], color["Blue"]


    def animate_move(self, direction):
        self.difference_list, self.spawned_tile = self.game.move(direction)

    def move(self, event):
        if event.key == K_UP:
            self.animate_move("up")
        if event.key == K_DOWN:
            self.animate_move("down")
        if event.key == K_LEFT:
            self.animate_move("left")
        if event.key == K_RIGHT:
            self.animate_move("right")


    def draw_bg(self):
        draw.rect(self.screen, self.get_color("background"), [self.padding, self.margin, 
            3 * (self.width + self.padding) + self.width, 3 * (self.width + self.padding) + self.width])

    
    def draw_topbar(self):
        txt_surface = font.SysFont(None, 80).render("2048", True, (0,0,0))
        rect_2048 = txt_surface.get_rect()
        self.screen.blit(txt_surface, Rect(self.padding, self.padding, 0, 0))
        #score is the sum of tiles on the screen
        score = sum([self.game.field[i][j] for i in range(4) for j in range(4)])
        txt_surface = font.SysFont(None, 40).render("SCORE: " + str(score), True, (0,0,0))
        txt_rect = txt_surface.get_rect()
        self.screen.blit(txt_surface, Rect(DrawGame.WIDTH - txt_rect.width - self.padding, rect_2048.height/2 + self.padding - txt_rect.height/2, 100, 100))

    def start(self):
        while True:
            if not self.game.game_is_running:
                print("You have lost!")
                self.game = Game()
            for i in event.get():  
                if i.type == QUIT:
                    sys.exit()
                if i.type == KEYDOWN and len(self.difference_list) == 0:
                    self.move(i)
            self.draw_topbar()
            self.draw_bg()
            if len(self.difference_list):
                self.animate()
            else:
                self.redraw(self.game.field)
            display.flip()
            self.clock.tick(60)
            self.screen.fill(self.get_color("dark-bg"))


    def animate(self):
        exluded_tiles = []
        animation_time = 200
        animation_time /= 60
        if self.frame_counter >= animation_time:
            self.frame_counter = 0
            self.difference_list = []
            if self.spawned_tile is not None:
                i, j = self.spawned_tile        # new tile appear!
                self.game.field[i][j] = Game.either_2_or_4()
                print(self.game)
                self.redraw(self.game.field, exluded_tiles)
                return
        for difference in self.difference_list:
            x1, y1, x2, y2 = difference
            exluded_tiles.append((x1,y1))
            tile_rect = Rect(self.padding + (x1 + (x2 - x1) * self.frame_counter / animation_time) * (self.width + self.padding), 
                self.margin + (y1 + (y2 - y1) * self.frame_counter / animation_time) * (self.width + self.padding), self.width, self.width)
            value = self.game.prev_state[y1][x1]
            draw.rect(self.screen, self.get_color(value), tile_rect)
            txt_surface = self.font.render(str(value), True, (255,255,255))
            text_rect = txt_surface.get_rect()
            self.screen.blit(txt_surface, [tile_rect.centerx - text_rect.width / 2, tile_rect.centery - text_rect.height / 2])
        self.redraw(self.game.prev_state, exluded_tiles)
        self.frame_counter += 1


    def redraw(self, array, exluded_tiles = []):       #exluded_tiles - not to draw animated tiles
        tiles = [(i,j) for i in range(4) for j in range(4) if (array[i][j] != 0 and (j,i) not in exluded_tiles)]
        for i,j in tiles:
            value = array[i][j]
            tile_rect = draw.rect(self.screen, self.get_color(value), Rect(self.padding + j * (self.width + self.padding), self.margin + i * (self.width + self.padding), self.width, self.width))
            txt_surface = self.font.render(str(value), True, (255,255,255))
            text_rect = txt_surface.get_rect()
            self.screen.blit(txt_surface, [tile_rect.centerx - text_rect.width / 2, tile_rect.centery - text_rect.height / 2])


if __name__ == "__main__":
    drawGame = DrawGame()
    print(drawGame.game)
    drawGame.start()
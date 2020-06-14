import numpy as np
from enum import Enum
from random import choice

class Move(Enum):
    left = 1
    right = 2
    down = 3
    up = 4
    exit = 5

class Game():
    def __init__(self):
        self.field = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ])
        self.spawn_tile()
        self.spawn_tile()
        self.switch = True
        self.game_is_running = True
        self.prev_state = []

    def rotate(self, move):
        if move == Move.left:
            return
        elif move == Move.right:
            self.field = np.fliplr(self.field)       # return flipped matrix (left to right) 
        elif move == Move.up:
            self.field = self.field.transpose()      # return transposed matrix
        elif move == Move.down and self.switch:      
            self.field = np.fliplr(self.field.transpose())
        else:
            self.field = np.fliplr(self.field).transpose()
        self.switch = not self.switch

    @staticmethod
    def difference(array1, array2):
        output = []
        i = 3
        start_ind = 5
        while i >= 0:
            j = min(i,start_ind)
            while j >= 0:
                if array1[i] == array2[j] or 2 * array1[i] == array2[j]:
                    output.append((i,j))
                    start_ind = j - 1
                    break
                j -= 1
            i -= 1
        return output


    @staticmethod
    def left_shift(line):
        line = list(line)
        def delete_zeros(list):
            while True:
                try:
                    list.remove(0)
                except ValueError as e:
                    break
            return list
        i = 0
        delete_zeros(line)
        while i <= len(line) - 2:
            if line[i] == line[i + 1]:
                line[i] *= 2
                line[i + 1] = 0
            i += 1
            delete_zeros(line)
        for i in range(4-len(line)):
            line.append(0)
        return line

    def spawn_tile(self):
        available_tiles = [(i,j) for i in range(4) for j in range(4) if self.field[i][j] == 0]
        i, j = choice(available_tiles)
        self.field[i][j] = 2

    def move(self, action):  #all inner logic is here
        try:
            move = Move[action]
        except KeyError:
            print("Type it correctly")
            return
        if Move[action] == Move.exit:
            self.game_is_running = False
            return
        
        self.prev_state = np.array(self.field)
        self.rotate(move)
        for i in range(4):
            temp_array = np.array(Game.left_shift(self.field[i]))
            print(Game.difference(self.field[i], temp_array))
            self.field[i] = temp_array        
        self.rotate(move)
        if (self.prev_state == self.field).all():
            print("nothing changed")
        else:
            self.spawn_tile()

    def __str__(self):
        return self.field.__str__() +"\n"

    def start_game(self):
        print("Type left, right, up, down or exit to play.")
        while self.game_is_running:
            print(g)
            action = input()
            g.move(action)


if __name__ == '__main__':
    g = Game()
    g.start_game()

    

import numpy as np
from enum import Enum
from random import choice, randint

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
        for i in range(2):
            i, j = self.spawn_tile()
            self.field[i][j] = 2
        # self.field = np.array([
        #     [2, 4, 8, 16],
        #     [32, 64, 128, 256],
        #     [512, 1024, 2048, 4096],
        #     [8192, 16, 32, 0],
        # ])
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
        for i in range(4 - len(line)):
            line.append(0)
        return line

    @staticmethod
    def difference(array1, array2, coord, move):    # 8 4 2 2
        array1_ind, array2_ind, output = [],[], []
        for ind, el in enumerate(array1):
            if el != 0:
                array1_ind.append(ind)
        for ind, el in enumerate(array2):
            if el != 0:
                array2_ind.append(ind)
        if len(array1_ind) == len(array2_ind):
            output = [(array1_ind[i],array2_ind[i]) for i in range(len(array1_ind))]
        else:
            i = 0
            it1 = iter(array1_ind)
            it2 = iter(array2_ind)
            while True:
                try:
                    ind1 = next(it1)
                    ind2 = next(it2)
                except StopIteration as e:
                    break
                if array1[ind1] == array2[ind2]:
                    output.append((ind1,ind2))
                else:
                    output.append((ind1,ind2))
                    output.append((next(it1),ind2))
        output = [out for out in output if out[0] != out[1]]
        if move == Move.down or move == Move.right:
            output = [(abs(3 - tupple[0]), abs(3 - tupple[1])) for tupple in output]
        if move == Move.down or move == Move.up:
            output = [(coord, tupple[0], coord, tupple[1]) for tupple in output]
        else:
            output = [(tupple[0], coord, tupple[1], coord) for tupple in output]
        return output



    def spawn_tile(self):
        available_tiles = [(i,j) for i in range(4) for j in range(4) if self.field[i][j] == 0]
        i, j = choice(available_tiles)
        return i, j

    def move(self, action):  #all inner logic is here
        try:
            move = Move[action]
        except KeyError:
            print("Type it correctly")
            return [], None
        if Move[action] == Move.exit or self.lose_condition():
            self.game_is_running = False
            return [], None
        self.prev_state = np.array(self.field)
        self.rotate(move)
        difference_list = []
        for i in range(4):
            temp_array = np.array(Game.left_shift(self.field[i]))
            difference_list += Game.difference(self.field[i], temp_array, i, move)
            self.field[i] = temp_array       
        # print(difference_list) 
        self.rotate(move)
        spawned_tile = None
        if (self.prev_state == self.field).all():
            print("nothing changed")
        else:
            spawned_tile = self.spawn_tile()
        return difference_list, spawned_tile

    def __str__(self):
        return self.field.__str__() +"\n"

    def lose_condition(self):
        difference_list = []
        for move in [Move.left, Move.right, Move.up, Move.down]:
            self.rotate(move) 
            for i in range(4):
                temp_array = np.array(Game.left_shift(self.field[i]))
                difference_list += Game.difference(self.field[i], temp_array, i, move)
            self.rotate(move)  
        return not len(difference_list)

    @staticmethod
    def either_2_or_4():
        return 4 if randint(0,9) == 0 else 2  # ratio is 1 to 9 

    def start_game(self):
        print("Type left, right, up, down or exit to play.")
        while self.game_is_running:
            print(self)
            action = input()
            _, spawned_tile = g.move(action)
            if spawned_tile is not None:
                i, j = spawned_tile
                self.field[i][j] = Game.either_2_or_4()
        print("You lost!")



if __name__ == '__main__':
    g = Game()
    g.start_game()

    

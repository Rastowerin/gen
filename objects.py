import random as r
from func import *


class Cell:

    p = 0
    m = [0] * 32
    for i in range(32):
        m[i] = r.randint(0, 31)
    health = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        m[self.x][self.y] = self
        cells.add(self)
        draw_cell(self.x, self.y)

    def __del__(self):
        clear(self.x, self.y)
        cells_to_del.add(self)

    def __repr__(self):
        return 'C'

    def delete(self):
        self.__del__()

    def coord(self, num, min):
        dx, dy = 0, 0

        if num in (min + 2, min + 3, min + 4):
            dx = 1

        if num in (min + 6, min + 7, min + 0):
            dx = -1

        if num in (min + 0, min + 1, min + 2):
            dy = 1

        if num in (min + 4, min + 5, min + 6):
            dy = -1

        return dx, dy

    def mutate(self):
        self.m[r.randint(0, 31)] = r.randint(0, 31)

    def replicate(self, a):
        for i in range(a):

            f = True
            while f:
                x, y = r.randint(1, 18), r.randint(1, 8)
                if m[x][y] == 0:
                    f = False

            Cell(x, y)
            m[x][y].m = self.m.copy()

            if i == a - 1:
                m[x][y].mutate()

    def go(self, num):

        dx, dy = self.coord(num, 0)

        if m[self.x + dx][self.y + dy] == 3:
            return

        if m[self.x + dx][self.y + dy] == 2:
            self.__del__()

        clear(self.x, self.y)
        self.x, self.y = self.x + dx, self.y + dy
        m[self.x][self.y] = self
        draw_cell(self.x, self.y)

    def look(self, num):
        dx, dy = self.coord(num, 8)
        
        if m[self.x + dx][self.y + dy].__class__ == Cell:
            return 4
        
        return m[self.x + dx][self.y + dy]

    def eat(self, num):
        dx, dy = self.coord(num, 16)

        if m[self.x + dx][self.y + dy] == 1:
            clear(self.x + dx, self.y + dy)
            self.health += 10
            return 0

        if m[self.x + dx][self.y + dy] == 2:
            clear(self.x + dx, self.y + dy)
            create_food(self.x + dx, self.y + dy)
            return 1

        return 2

    def turn(self):

        self.health -= 1
        if self.health == 0:
            self.__del__()

        count = 0
        while count < 10:
            num = self.m[self.p]

            if num < 8:
                self.go(num)

                self.p = (self.p + 1) % 32
                break

            elif num < 16:
                res = self.look(num)
                dp = [1, 4, 7, 10, 13, 16]

                self.p = (self.p + dp[res]) % 32
                count += 1

            elif num < 24:
                res = self.eat(num)
                dp = [1, 3, 5]

                self.p = (self.p + dp[res]) % 5
                break

            elif num < 32:
                self.p = (self.p + (num - 24)) % 32
                count += 1

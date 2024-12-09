import random
import os


class Player():
    def __init__(self, n):
        self.n = n
        self.user1 = ''
        self.user2 = ''
        self.board = [['-' for _ in range(self.n)] for _ in range(self.n)]
        self.step = 0

    def __str__(self):
        s = '   1 | 2 | 3 |\n'
        for i in range(self.n):
            s += str(i + 1) + '|'
            for j in range(self.n):
                s += ' ' + self.board[i][j] + ' |'
            s += '\n'
        return s

    def check_all(self):
        count = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] != '-':
                    count += 1
        if count == 9:
            return False
        else:
            return True

    def check_gor(self):
        for i in range(self.n):
            if self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2] \
                    and self.board[i][0] != '-':
                return False
        return True

    def check_vert(self):
        for j in range(self.n):
            if self.board[0][j] == self.board[1][j] and self.board[1][j] == self.board[2][j] \
                    and self.board[0][j] != '-':
                return False
        return True

    def check_diag(self):
        if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[0][0] != '-':
            return False
        elif self.board[2][0] == self.board[1][1] and self.board[2][0] == self.board[0][2] and self.board[1][1] != '-':
            return False
        else:
            return True

    def update_matrix(self):
        os.system("cls")
        print(self)
            
    def step_game(self, user):
        row = int(input('Введите строку: ')) - 1
        col = int(input('Введите колонку: ')) - 1
        if self.board[row][col] != '-':
            print('Так нельзя ходить')
        else:
            self.board[row][col] = user
            self.step += 1
        Player.update_matrix(self)

    def go(self):
        Player.update_matrix(self)
        # определяем кто будет ходить первым? (random) если 1 - Х, иначе 0 в self.user1
        first = random.randint(0, 1)
        if first == 0:
            self.user1 = '0'
            self.user2 = 'X'
        else:
            self.user1 = 'X'
            self.user2 = '0'
        # игра начинается
        # пока один из 4 вариантов не сработает:
        # WHILE
        # False - значит финиш, кто-то выиграл или ничья
        #1 - где-то по горизонтали не соберётся комбинаци,
        #2 - где-то по вертикали не соберётся комбинаци,
        #3 - где-то по диагонали не соберётся комбинаци,
        while Player.check_gor(self) is True and Player.check_vert(self) is True and Player.check_diag(self) is True \
                and Player.check_all(self) is True:
            if self.step % 2 == 0:
                print('Ходит', self.user1)
                Player.step_game(self, self.user1)
            else:
                print('Ходит', self.user2)
                Player.step_game(self, self.user2)
        if Player.check_all(self) is False:
            print('Ничья')
        else:
            if self.step % 2 == 0:
                print('Выиграл', self.user2)
            else:
                print('Выиграл', self.user1)


        #4 - пока все 9 будут не заполнены,
        #---

            #если self.step - чётный, то ходит первый, то есть self.user1
            #---
            # шаг игры
            # ---
            # self.step += 1

        # определить победителя
        # self.step == 9 - ничья
        # если self.step - чётный, то победил self.user1

N = int(input('Введите размер поля: '))
play = Player(N)
play.go()


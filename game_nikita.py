import random


class Player:
    def __init__(self, n):
        self.n = n
        self.user1 = ''
        self.user2 = ''
        self.board = [['-' for _ in range(self.n)] for _ in range(self.n)]
        self.step = 0

    def __str__(self):
        s = '   ' + f'{" | ".join(str(i) for i in range(1, self.n+1))}' + '\n'
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
        if count == self.n**2:
            return False
        else:
            return True

    def check_gor(self):
        for i in range(self.n):
            if len(set(self.board[i][j] for j in range(self.n))) == 1 and self.board[i][0] != '-':
                return False
        return True

    def check_vert(self):
        for j in range(self.n):
            if len(set(self.board[i][j] for i in range(self.n))) == 1 and self.board[0][j] != '-':
                return False
        return True

    def check_diag(self):
        j = self.n - 1
        set_diag = set()
        for i in range(self.n):
            set_diag.add(self.board[i][j])
            j -= 1
        if (len(set(self.board[i][i] for i in range(self.n))) == 1 and self.board[0][0] != '-') \
           or (len(set_diag) == 1 and self.board[0][self.n-1] != '-'):
            return False
        else:
            return True
            
    def step_game(self, user):
        if user == self.user1:
            row = int(input('Введите строку: ')) - 1
            col = int(input('Введите колонку: ')) - 1
        else:
            right_combs = [(i, j) for j in range(self.n) for i in range(self.n) if self.board[i][j] == '-']
            row, col = random.choice(right_combs)
        if self.board[row][col] != '-':
            print('Так нельзя ходить')
        else:
            self.board[row][col] = user
            self.step += 1
        print(self)

    def go(self):
        print(self)
        # определяем кто будет ходить первым? (random) если 1 - Х, иначе 0 в self.user1
        first = random.randint(0, 1)
        if first == 0:
            self.user1 = 'O'
            self.user2 = 'X'
        else:
            self.user1 = 'X'
            self.user2 = 'O'
        # игра начинается
        # пока один из 4 вариантов не сработает:
        # WHILE
        # False - значит финиш, кто-то выиграл или ничья
        #1 - где-то по горизонтали не соберётся комбинаци,
        #2 - где-то по вертикали не соберётся комбинаци,
        #3 - где-то по диагонали не соберётся комбинаци,
        while all((Player.check_gor(self), Player.check_vert(self), Player.check_diag(self), Player.check_all(self))):
            if self.step % 2 == 0:
                print(f'Ходит "{self.user1}"')
                Player.step_game(self, self.user1)
            else:
                print(f'"{self.user2}" сходил')
                Player.step_game(self, self.user2)
        if Player.check_all(self) is False:
            print('Ничья')
        else:
            if self.step % 2 == 0:
                print(f'Выиграл "{self.user2}"')
            else:
                print(f'Выиграл "{self.user1}"')


        # - пока все поля будут не заполнены,
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


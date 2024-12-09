import os


class Game:
    def __init__(self) -> None:

        # Символы крестиков, ноликов и пустых клеток
        self.zero  : str = "O"
        self.cross : str = "X"
        empty : str = " "
        vert_bord : str = "|"
        horiz_bord : str = "_"
        
        # Настоящий игрок
        self.current_player : str = self.zero
        
        # Генерация пустой матрицы [[" ","_","_","_"," "],["|"," "," "," ","|"],["|"," "," "," ","|"],["|"," "," "," ","|"],[" ","_","_","_"," "]]
        self.box : list[list[str]] = [
            [empty, horiz_bord, horiz_bord, horiz_bord, empty],
            [vert_bord, empty, empty, empty,vert_bord],
            [vert_bord, empty, empty, empty,vert_bord],
            [vert_bord, empty, empty, empty,vert_bord],
            [empty, horiz_bord, horiz_bord, horiz_bord, empty]
        ]
    
    def run(self) -> None:
        # Вызов обновления и вывод матрицы
        self.update_matrix()

        while True:
            x, y = map(int, input(f" > Введите координаты {self.current_player} (через пробел): ").split())

            if (y in [1, 2, 3]) and (x in [1, 2, 3]):
                self.box[y][x] = self.current_player
                if self.current_player == self.zero: 
                    self.current_player = self.cross
                else:
                    self.current_player = self.zero

            # Вызов обновления и вывод матрицы
            self.update_matrix()

            if (y not in [1, 2, 3]) and (x not in [1, 2, 3]):
                print("Выход за рамки")

    def update_matrix(self) -> None:
        os.system("clear")
        for y in range(5):
            # Создаём список значений строки поля и объединяем её
            string = "".join([self.box[y][x] for x in range(5)])
            print(string)

if __name__ == "__main__":
    # Запуск игры
    new_game : Game = Game()
    new_game.run()

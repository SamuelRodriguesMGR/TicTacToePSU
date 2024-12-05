
import os


class Game:
    def __init__(self) -> None:

        # Символы крестиков, ноликов и пустых клеток
        self.empty : str = " "
        self.zero  : str = "O"
        self.cross : str = "X"
        
        # Настоящий игрок
        self.current_player : str = self.zero
        
        # Генерация пустой матрицы [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.box : list[list[str]] = [[self.empty for i in range(3)] for j in range(3)]
    
    def run(self) -> None:
        # Вызов обновления и вывод матрицы
        self.update_matrix()

        while True:
            x, y = map(int, input(f" > Введите координаты {self.current_player} (через пробел): ").split())
            self.box[y][x] = self.current_player

            # Вызов обновления и вывод матрицы
            self.update_matrix()

            if self.current_player == self.zero: 
                self.current_player = self.cross
            else:
                self.current_player = self.zero

    def update_matrix(self) -> None:
        os.system("clear")
        for y in range(3):
            # Создаём список значений строки поля и объединяем её
            string = "|".join([self.box[y][x] for x in range(3)])
            print(string)

if __name__ == "__main__":
    # Запуск игры
    new_game : Game = Game()
    new_game.run()


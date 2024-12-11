
import pygame
import random
import time

BLACK : int = (0, 0, 0)
WHITE : int = (255, 255, 255)
RED   : int = (255, 0, 0)
BLUE  : int = (0, 0, 255)

class Game:
    def __init__(self) -> None:

        pygame.init()
        pygame.display.set_caption("Pygame Tic Tac Toe")

        size_field = input(" > Введите размер поля (от 1 до 10): ")

        self.SIZE_FIELD     : int  = int(size_field) if size_field in [str(i) for i in range(1, 11)] else 3
        self.HEIGHT         : int  = 600
        self.WIDTH          : int  = int(self.HEIGHT // self.SIZE_FIELD + self.HEIGHT)
        self.FPS            : int  = 30
        self.CELL_SIZE      : int  = self.HEIGHT // self.SIZE_FIELD # размер яйчеек
        self.LINE_THICKNESS : int  = 1   # размер толщины линии
        self.LABEL_SIZE     : int  = int(self.CELL_SIZE * 0.75) # размер иконок

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock  = pygame.time.Clock()

        # фон
        self.Background = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.Background.fill(BLACK)
        
        self._new_game()

    def _new_game(self) -> None:
        self.winner : str = ""
        self.field_cell = [[[x, y, " "] for x in range(self.SIZE_FIELD)] for y in range(self.SIZE_FIELD)]
        # рандом кто начинает
        self.order_steps : list = ["X", "O"]
        random.shuffle(self.order_steps)
        self.current_character : str = "player" if self.order_steps[0] == "O" else "bot"
        # прикольная табличка
        self.size_font = int(self.CELL_SIZE * 0.18)
        self.font = pygame.font.Font(None, self.size_font)
        self.current_text = "Удачной игры"
        time.sleep(0.1)

    def run(self) -> None: 

        running = True
        while running:

            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False


            mouse_pressed  = pygame.mouse.get_pressed()
            mouse_position = pygame.mouse.get_pos()
            x : int = int(mouse_position[0] / self.CELL_SIZE)
            y : int = int(mouse_position[1] / self.CELL_SIZE)


            # ставим фон
            self.screen.blit(self.Background, (0, 0))
            # ставим текст
            text_surface = self.font.render(self.current_text, True, WHITE)
            text_rect = text_surface.get_rect(topleft=(self.CELL_SIZE * self.SIZE_FIELD + 5, 10))
            self.screen.blit(text_surface, text_rect)
            # ставим яйчейки
            for row in self.field_cell:
                for cell in row:
                    self._update_map(cell)
            # ставим кнопку рестарта
            self.button_restart(self.SIZE_FIELD, self.SIZE_FIELD - 1, [x, y, mouse_pressed[0]])

            pygame.display.flip()

            # игровой процесс
            if mouse_pressed[0] and (x in range(self.SIZE_FIELD)) and (y in range(self.SIZE_FIELD)) and\
                    self.field_cell[y][x][2] == " " and self.current_character == "player" and not self.winner:
                self._put_label(x, y, "O")
                
                if not self._check_all_conditions():
                    self.winner = "player"

            if self._check_all() and self.current_character == "bot" and not self.winner:
                self._step_bot()

                if not self._check_all_conditions():
                    self.winner = "bot"

             # победа
            if self.winner:
               
                if not self._check_hor() or not self._check_diag() or not self._check_vert():
                    self._set_text(f"Победил {self.winner}")

                else:
                    self._set_text(f"Победила дружба")

            
        pygame.quit()

    def button_restart(self, x, y, mouse_data) -> None:
        size_button_x, size_button_y = self.CELL_SIZE // 2, int(self.CELL_SIZE * 0.4)
        center = self.CELL_SIZE // 2
        pygame.draw.rect(self.screen, WHITE, 
        (x * self.CELL_SIZE + center - size_button_x // 2, 
         y * self.CELL_SIZE + center - size_button_y // 2, 
        size_button_x, size_button_y))
        # текст
        text_surface = self.font.render("Рестарт", True, BLACK)
        text_rect = text_surface.get_rect(topleft=(self.CELL_SIZE * x + center - size_button_x // 2 + 4, self.CELL_SIZE * y + center - size_button_y // 2 + 25))
        self.screen.blit(text_surface, text_rect)
        
        if mouse_data[0] == x and mouse_data[1] == y and mouse_data[2]:
            self._new_game()

    def _update_map(self, cell) -> None:
        position_x = cell[0] * self.CELL_SIZE
        position_y = cell[1] * self.CELL_SIZE

        # отрисовка каждой яйчейки
        pygame.draw.rect(self.screen, WHITE, (position_x, position_y, self.CELL_SIZE, self.CELL_SIZE), self.LINE_THICKNESS)

        if cell[2] == "X":
            # Если коротко, это формула берёт центр яйчеки (position_x + self.CELL_SIZE // 2), а потом уводит x и y в правильные координаты
            center_cell_x = position_x + self.CELL_SIZE // 2
            center_cell_y = position_y + self.CELL_SIZE // 2

            pygame.draw.line(self.screen, WHITE, 
                             (center_cell_x - self.LABEL_SIZE // 2, center_cell_y - self.LABEL_SIZE // 2), 
                             (center_cell_x + self.LABEL_SIZE // 2, center_cell_y + self.LABEL_SIZE // 2), 
                             self.LINE_THICKNESS)
            
            pygame.draw.line(self.screen, WHITE, 
                             (center_cell_x + self.LABEL_SIZE // 2, center_cell_y - self.LABEL_SIZE // 2), 
                             (center_cell_x - self.LABEL_SIZE // 2, center_cell_y + self.LABEL_SIZE // 2),
                             self.LINE_THICKNESS)
        elif cell[2] == "O":
            # рисует круг
            pygame.draw.circle(self.screen, WHITE, 
                               (position_x + self.CELL_SIZE // 2, 
                                position_y + self.CELL_SIZE // 2), 
                               self.LABEL_SIZE // 2, self.LINE_THICKNESS)

    def _put_label(self, x, y, label) -> None:
        # изменяем статус яйчейки
        self.field_cell[y][x][2] = label
        self.current_character = "player" if self.current_character == "bot" else "bot"

    def _step_bot(self) -> None:
        # ищем пустые для бота яйчейки
        empty_cells = [[cell for cell in row if cell[2] == " "] for row in self.field_cell if [cell for cell in row if cell[2] == " "] != []]
        x, y, label = random.choice(random.choice(empty_cells))
        self._put_label(x, y, "X")

    def _check_all(self) -> bool:
        # проверка полное ли поле
        for row in self.field_cell:
            for cell in row:
                if cell[2] == " ":
                    return True
        return False

    def _check_hor(self):
        for i in range(self.SIZE_FIELD):
            if len(set(self.field_cell[i][j][2] for j in range(self.SIZE_FIELD))) == 1 and self.field_cell[i][0][2] != ' ':
                return False
        return True
    
    def _check_vert(self):
        for j in range(self.SIZE_FIELD):
            if len(set(self.field_cell[i][j][2] for i in range(self.SIZE_FIELD))) == 1 and self.field_cell[0][j][2] != ' ':
                return False
        return True

    def _check_diag(self):
        if len(set(self.field_cell[i][i][2] for i in range(self.SIZE_FIELD))) == 1 and self.field_cell[0][0][2] != ' ' \
            or len(set(self.field_cell[i][self.SIZE_FIELD - i - 1][2] for i in range(self.SIZE_FIELD))) == 1 and self.field_cell[self.SIZE_FIELD - 1][0][2] != ' ':
            return False
        return True


        # j = self.SIZE_FIELD - 1
        # set_diag = set()
        # for i in range(self.SIZE_FIELD):
        #     set_diag.add(self.field_cell[i][j][2])
        #     j -= 1
        # if (len(set(self.field_cell[i][i][2] for i in range(self.SIZE_FIELD))) == 1 and self.field_cell[0][0][2] != ' ') \
        #    or (len(set_diag) == 1 and self.field_cell[0][self.SIZE_FIELD - 1] != ' '):
        #     return False
        # else:
        #     return True

    def _check_all_conditions(self) -> bool:
        return all((self._check_hor(), self._check_vert(), self._check_diag(), self._check_all()))

    def _set_text(self, new_text : str) -> None:
        self.current_text = new_text


if __name__ == "__main__":
    # Запуск игры
    new_game : Game = Game()
    new_game.run()




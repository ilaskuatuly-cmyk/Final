init python:
    import random
    import renpy.store as store

    class Game2048:
        def __init__(self):
            self.grid = [[0 for _ in range(4)] for _ in range(4)]
            self.score = 0
            self.timer = 90.0
            self.game_over = False
            self.win = False
            self.max_tile = 0
            self.spawn_tile()
            self.spawn_tile()

        def spawn_tile(self):
            empty_cells = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
            if empty_cells:
                r, c = random.choice(empty_cells)
                self.grid[r][c] = 2 if random.random() < 0.9 else 4
                self.update_max_tile()

        def update_max_tile(self):
            # Calculate max tile value in the current grid
            current_max = 0
            for row in self.grid:
                for val in row:
                    if val > current_max:
                        current_max = val
            self.max_tile = current_max
            
            if self.max_tile >= 256:
                self.win = True
                self.game_over = True

        def compress(self, row):
            new_row = [i for i in row if i != 0]
            new_row += [0] * (4 - len(new_row))
            return new_row

        def merge(self, row):
            for i in range(3):
                if row[i] == row[i+1] and row[i] != 0:
                    row[i] *= 2
                    row[i+1] = 0
            return row

        def _move_logic(self):
            moved = False
            for i in range(4):
                old_row = list(self.grid[i])
                row = self.compress(self.grid[i])
                row = self.merge(row)
                row = self.compress(row)
                self.grid[i] = row
                if old_row != self.grid[i]:
                    moved = True
            return moved

        def move(self, direction):
            """
            Main entry point for movement. Handles direction, spawning, 
            game over checks, and UI refresh.
            Returns None to prevent Ren'Py from closing the screen.
            """
            if self.game_over:
                return

            moved = False
            if direction == "left":
                moved = self._move_logic()
            elif direction == "right":
                self.reverse_grid()
                moved = self._move_logic()
                self.reverse_grid()
            elif direction == "up":
                self.transpose_grid()
                moved = self._move_logic()
                self.transpose_grid()
            elif direction == "down":
                self.transpose_grid()
                self.reverse_grid()
                moved = self._move_logic()
                self.reverse_grid()
                self.transpose_grid()

            if moved:
                self.spawn_tile()
                self.check_game_over()
            
            # Обновляем максимальную плитку в любом случае для UI
            self.update_max_tile()
            
            # Важно: заставляем Ren'Py перерисовать экран
            renpy.restart_interaction()
            return None # Явно возвращаем None

        def transpose_grid(self):
            self.grid = [list(row) for row in zip(*self.grid)]

        def reverse_grid(self):
            for i in range(4):
                self.grid[i].reverse()

        def check_game_over(self):
            # Check for empty spaces
            if any(0 in row for row in self.grid):
                return False
            # Check for possible horizontal merges
            for r in range(4):
                for c in range(3):
                    if self.grid[r][c] == self.grid[r][c+1]:
                        return False
            # Check for possible vertical merges
            for r in range(3):
                for c in range(4):
                    if self.grid[r][c] == self.grid[r+1][c]:
                        return False
            self.game_over = True
            return True

        def get_final_score(self):
            """
            Расчет итогового балла (0-100) на основе максимальной плитки.
            Используется нелинейная шкала:
            2   -> 0 
            4   -> 5 
            8   -> 15 
            16  -> 30 
            32  -> 45 
            64  -> 60 
            128 -> 80 
            256 -> 100
            """
            if self.win or self.max_tile >= 256:
                return 100
            
            # Таблица соответствия плитки и баллов
            scores_map = {
                2: 0,
                4: 5,
                8: 15,
                16: 30,
                32: 45,
                64: 60,
                128: 80,
                256: 100
            }
            
            return scores_map.get(self.max_tile, 0)

label run_exam_math:
    python:
        math_game = Game2048()
    
    "Экзамен: Математический анализ"
    "Задача: Решите головоломку 2048 (Версия с ограничением времени)."
    "Цель: Достигните плитки со значением 256 за 90 секунд."
    "Управление: Клавиши со стрелками или кнопки на экране."
    
    window hide
    call screen math_2048_screen(math_game)
    
    $ final_score = math_game.get_final_score()
    
    if math_game.win or math_game.max_tile >= 256:
        "Блестяще! Вы достигли 256!"
    elif _return == "skip":
        $ final_score = 0
        "Экзамен пропущен. (0 баллов)"
    else:
        "Экзамен завершен."
        "Максимальная плитка: [math_game.max_tile]."
    
    $ store.exam_grades["math_analysis"] = final_score
    return final_score

screen math_2048_screen(game):
    # Таймер
    if not game.game_over:
        timer 0.1 repeat True action [
            SetField(game, "timer", game.timer - 0.1),
            If(game.timer <= 0, [SetField(game, "game_over", True)])
        ]
    
    if game.game_over:
        timer 1.5 action Return()

    # Управление с клавиатуры
    key "K_LEFT" action Function(game.move, "left")
    key "K_RIGHT" action Function(game.move, "right")
    key "K_UP" action Function(game.move, "up")
    key "K_DOWN" action Function(game.move, "down")

    add "#1a1a2e"
    
    vbox:
        xalign 0.5
        ypos 50
        spacing 20
        
        frame:
            background "#16213e"
            padding (20, 10)
            xalign 0.5
            hbox:
                spacing 40
                vbox:
                    text "ВРЕМЯ":
                        size 18
                        color "#888"
                        xalign 0.5
                    text "[game.timer:.1f]с":
                        size 32
                        color "#e94560"
                        bold True
                vbox:
                    text "МАКС. ПЛИТКА":
                        size 18
                        color "#888"
                        xalign 0.5
                    text "[game.max_tile]":
                        size 32
                        color "#f1faee"
                        bold True
        
        # Сетка 2048
        frame:
            background "#2c3e50"
            padding (10, 10)
            xalign 0.5
            
            grid 4 4:
                spacing 10
                for r in range(4):
                    for c in range(4):
                        $ val = game.grid[r][c]
                        $ tile_colors = {
                            0: "#34495e",
                            2: "#ecf0f1",
                            4: "#bdc3c7",
                            8: "#f39c12",
                            16: "#e67e22",
                            32: "#e74c3c",
                            64: "#c0392b",
                            128: "#f1c40f",
                            256: "#f1c40f"
                        }
                        $ t_color = tile_colors.get(val, "#f1c40f")
                        $ text_c = "#2c3e50" if val <= 4 else "#fff"
                        
                        frame:
                            xsize 100
                            ysize 100
                            background t_color
                            if val > 0:
                                text str(val):
                                    align (0.5, 0.5)
                                    size 36
                                    bold True
                                    color text_c

    # Кнопки управления (для мыши)
    hbox:
        xalign 0.5
        ypos 720
        spacing 10
        
        grid 3 3:
            spacing 5
            null
            textbutton "↑":
                action Function(game.move, "up")
                style "math_control_button"
            null
            
            textbutton "←":
                action Function(game.move, "left")
                style "math_control_button"
            null
            textbutton "→":
                action Function(game.move, "right")
                style "math_control_button"
                
            null
            textbutton "↓":
                action Function(game.move, "down")
                style "math_control_button"
            null

    # Кнопка пропуска
    textbutton "Пропустить экзамен":
        align (0.95, 0.05)
        action Return("skip")
        text_size 18
        text_color "#fff"
        background "#e94560"
        padding (10, 5)

init:
    style math_control_button:
        background "#457b9d"
        hover_background "#1d3557"
        padding (5, 5)
        xsize 80
        ysize 80
        
    style math_control_button_text:
        color "#fff"
        size 32
        bold True
        align (0.5, 0.5)

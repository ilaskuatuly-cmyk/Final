init python:
    import time
    import copy
    import renpy.store as store

    class RobotGrid:
        def __init__(self, level_layout):
            self.width = len(level_layout[0])
            self.height = len(level_layout)
            self.grid = level_layout
            self.original_robot_pos = self.find_char('S')
            self.robot_pos = self.original_robot_pos
            self.robot_dir = 0  # 0=Right, 1=Down, 2=Left, 3=Up
            self.goal_pos = self.find_char('G')
            self.commands = []
            self.execution_index = 0
            self.is_executing = False
            self.status = "Editing"  # Editing, Executing, Win, Fail
            self.history = []
            
            # Валидация уровня
            self.validate_level()
            
        def validate_level(self):
            """Проверяет корректность уровня"""
            start_count = sum(row.count('S') for row in self.grid)
            goal_count = sum(row.count('G') for row in self.grid)
            
            if start_count != 1:
                raise ValueError("Уровень должен содержать ровно один старт (S)")
            if goal_count != 1:
                raise ValueError("Уровень должен содержать ровно одну цель (G)")
                
        def find_char(self, c):
            for y in range(self.height):
                for x in range(self.width):
                    if self.grid[y][x] == c:
                        return (x, y)
            return (0, 0)
            
        def add_command(self, cmd):
            """Добавляет команду в программу"""
            if len(self.commands) < 12:
                self.commands.append(cmd)
                
        def insert_command(self, index, cmd):
            """Вставляет команду на указанную позицию"""
            if len(self.commands) < 12 and 0 <= index <= len(self.commands):
                self.commands.insert(index, cmd)
                
        def remove_command(self, index):
            """Удаляет команду по индексу"""
            if 0 <= index < len(self.commands):
                self.commands.pop(index)
                
        def clear_commands(self):
            """Очищает программу"""
            self.commands = []
            self.reset_robot()
            
        def reset_robot(self):
            """Сбрасывает робота в начальное состояние"""
            self.robot_pos = self.original_robot_pos
            self.robot_dir = 0
            self.status = "Editing"
            self.execution_index = 0
            self.is_executing = False
            self.history = []
            
        def check_collision(self, x, y):
            """Проверяет, можно ли переместиться в клетку"""
            if not (0 <= x < self.width and 0 <= y < self.height):
                return True  # Выход за границы
            if self.grid[y][x] == '#':
                return True  # Стена
            return False
            
        def execute_next_step(self):
            """Выполняет один шаг программы"""
            if self.status in ["Win", "Fail"]:
                return False
                
            if not self.is_executing:
                self.is_executing = True
                self.status = "Executing"
                self.execution_index = 0
                
            if self.execution_index >= len(self.commands):
                self.status = "Fail"
                self.is_executing = False
                return False
                
            cmd = self.commands[self.execution_index]
            
            # Выполняем обычную команду
            result = self.execute_single_command(cmd)
            
            # Обновляем историю для анимации
            self.history.append({
                "pos": self.robot_pos,
                "dir": self.robot_dir,
                "cmd": cmd,
                "index": self.execution_index
            })
            
            self.execution_index += 1
                
            # Проверяем условия завершения
            if self.robot_pos == self.goal_pos:
                self.status = "Win"
                self.is_executing = False
                return False
                
            if self.execution_index >= len(self.commands):
                self.status = "Fail"
                self.is_executing = False
                return False
                
            return True
            
        def execute_single_command(self, cmd):
            """Выполняет одну команду движения"""
            x, y = self.robot_pos
            dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][self.robot_dir]
            
            if cmd == "Forward":
                nx, ny = x + dx, y + dy
                if not self.check_collision(nx, ny):
                    self.robot_pos = (nx, ny)
                    return True
                else:
                    self.status = "Fail"
                    return False
                    
            elif cmd == "Turn Left":
                self.robot_dir = (self.robot_dir - 1) % 4
                return True
                
            elif cmd == "Turn Right":
                self.robot_dir = (self.robot_dir + 1) % 4
                return True
                
            return False
            
        def execute_full_program(self):
            """Выполняет всю программу для проверки"""
            original_state = (self.robot_pos, self.robot_dir, self.status)
            self.reset_robot()
            
            steps = 0
            max_steps = 100  # Защита на всякий случай
            
            while steps < max_steps and self.status not in ["Win", "Fail"]:
                if not self.execute_next_step():
                    break
                steps += 1
                
            result = self.status == "Win"
            
            # Восстанавливаем состояние для отображения
            self.robot_pos, self.robot_dir, self.status = original_state
            self.is_executing = False
            
            return result
    def get_command_icon(cmd):
        icons = {
            "Forward": "→",
            "Turn Left": "↰",
            "Turn Right": "↱"
        }
        return icons.get(cmd, "?")

    # Основная функция запуска мини-игры
    def run_minigame_programming():
        score = 0
        max_score = 100
        
        narrator("Мини-игра: Программирование робота")
        _window_hide()
        narrator("Создайте программу для перемещения робота к цели.")
        
        # Уровень 1: Простой путь
        narrator("Уровень 1: Прямой путь к цели")
        level1 = [
            ".....",
            "S...G",
            "....."
        ]
        
        res = renpy.call_screen("robot_minigame_screen", level_data=level1, level_name="Уровень 1")
        if res == "skip":
            score += 0 # Пропуск не дает очков
            narrator("Уровень пропущен.")
        elif res is True:
            score += 30
            narrator("Отлично! Уровень 1 пройден.")
        else:
            narrator("Уровень 1 не пройден. Попробуйте еще раз позже.")
            return score
            
        # Уровень 2: Обход препятствий (сложнее)
        narrator("Уровень 2: Обход препятствия")
        narrator("Робот должен обойти стену справа.")
        level2 = [
            "..G..",
            ".#.#.",
            ".#.#.",
            "S...."
        ]
        
        # Помощь Аяна: первые ДВЕ правильные команды заранее выставлены
        # (только если игрок ранее получил помощь)
        prefill_level2 = ["Forward", "Forward"] if store.helped_ayan else None
        res = renpy.call_screen("robot_minigame_screen", level_data=level2, level_name="Уровень 2", prefill_commands=prefill_level2)
        if res == "skip":
            score += 0
            narrator("Уровень пропущен.")
        elif res is True:
            score += 35
            narrator("Прекрасно! Уровень 2 пройден.")
        else:
            narrator("Уровень 2 не пройден.")
            return score
            
        # Уровень 3: Более сложный лабиринт
        narrator("Уровень 3: Сложный маршрут")
        narrator("Найдите путь через лабиринт.")
        level3 = [
            "G...#",
            "##.#.",
            "...#.",
            ".#...",
            "S..##"
        ]
        
        res = renpy.call_screen("robot_minigame_screen", level_data=level3, level_name="Уровень 3")
        if res == "skip":
            score += 0
            narrator("Уровень пропущен.")
        elif res is True:
            score += 35
            narrator("Потрясающе! Все уровни пройдены!")
        else:
            narrator("Уровень 3 не пройден.")
            
        return score

# Стили должны быть объявлены в init block, а не внутри python block
init:
    style robot_exam_button:
        background "#3498db"
        hover_background "#2980b9"
        padding (25, 10)
        xsize 220
        
    style robot_exam_button_text:
        color "#fff"
        size 22
        bold True
        
    style robot_command_button:
        background "#2ecc71"
        hover_background "#27ae60"
        padding (20, 10)
        xsize 120
        
    style robot_control_button:
        background "#e74c3c"
        hover_background "#c0392b"
        padding (20, 10)
        xsize 120
        
    style robot_run_button:
        background "#9b59b6"
        hover_background "#8e44ad"
        padding (25, 10)
        xsize 200

    # Анимации для экрана мини-игры
    transform robot_panel_slide_in(delay=0.0, offset=60):
        alpha 0.0
        yoffset offset
        pause delay
        parallel:
            linear 0.35 alpha 1.0
        parallel:
            easeout 0.35 yoffset 0

    transform robot_goal_pulse():
        alpha 1.0
        linear 0.8 alpha 0.6
        linear 0.8 alpha 1.0
        repeat

    transform robot_pos_blink():
        alpha 1.0
        linear 0.25 alpha 0.5
        linear 0.25 alpha 1.0
        repeat

# Основной экран мини-игры
screen robot_minigame_screen(level_data, level_name="Уровень", prefill_commands=None):
    default grid = RobotGrid(level_data)
    default message = ""
    default message_timer = 0
    default show_help = False
    default executing_all = False
    default prefill_applied = False
    
    # Таймер для автоматического скрытия сообщений
    if message_timer > 0:
        timer 2.0 action [SetScreenVariable("message", ""), SetScreenVariable("message_timer", 0)]
    
    # Таймер для автоматического выполнения программы
    if executing_all and grid.is_executing and grid.status not in ["Win", "Fail"]:
        timer 0.5 action Function(grid.execute_next_step) repeat True
    elif executing_all:
        # Завершили выполнение
        timer 0.1 action SetScreenVariable("executing_all", False)
    
    # Помощь: предварительно заполнить команды (только один раз)
    if prefill_commands and not prefill_applied:
        python:
            for cmd in prefill_commands:
                grid.add_command(cmd)
        $ prefill_applied = True
    
    add "#2c3e50"
    
    # Верхняя панель с информацией
    frame at robot_panel_slide_in(0.0, 40):
        xalign 0.5
        ypos 20
        xsize 800
        background "#34495e"
        padding (20, 10)
        
        hbox:
            xalign 0.5
            spacing 40
            
            vbox:
                text level_name:
                    size 36
                    color "#fff"
                    bold True
                    
                text "Статус: [grid.status]":
                    size 24
                    color "#ecf0f1"
                    
            vbox:
                text "Команд: [len(grid.commands)]/12":
                    size 24
                    color "#ecf0f1"
                    
                if grid.is_executing:
                    text "Шаг: [grid.execution_index + 1]/[len(grid.commands)]":
                        size 24
                        color "#f1c40f"
    
    # Игровое поле
    frame at robot_panel_slide_in(0.08, 80):
        xalign 0.5
        ypos 120
        background "#34495e"
        padding (10, 10)
        
        # Отображение сетки
        grid grid.width grid.height:
            spacing 3
            for y in range(grid.height):
                for x in range(grid.width):
                    python:
                        cell = grid.grid[y][x]
                        
                        # Определяем цвет и символ для клетки
                        bg_color = "#95a5a6"  # Пустая
                        cell_text = ""
                        text_color = "#fff"
                        
                        if cell == '#':
                            bg_color = "#2c3e50"  # Стена
                        elif cell == 'S':
                            bg_color = "#27ae60"  # Старт
                        elif cell == 'G':
                            bg_color = "#e74c3c"  # Цель
                        
                        # Если здесь робот
                        if (x, y) == grid.robot_pos:
                            bg_color = "#f39c12"  # Робот
                            dir_symbols = ["→", "↓", "←", "↑"]
                            cell_text = dir_symbols[grid.robot_dir]
                            text_color = "#000"
                    
                    # Рамка для клетки
                    frame:
                        xsize 70
                        ysize 70
                        background bg_color
                        
                        if cell_text:
                            text cell_text:
                                align (0.5, 0.5)
                                size 40
                                color text_color
                                bold True
                        if cell == 'G':
                            add Solid("#ffffff55") at robot_goal_pulse()
                        if (x, y) == grid.robot_pos:
                            add Solid("#00000033") at robot_pos_blink()
    
    # Панель команд
    frame at robot_panel_slide_in(0.16, 80):
        xalign 0.5
        ypos 450
        xsize 900
        background "#34495e"
        padding (20, 20)
        
        vbox:
            spacing 15
            
            # Надпись
            text "Доступные команды:":
                size 28
                color "#ecf0f1"
                xalign 0.5
                
            # Кнопки команд
            hbox:
                xalign 0.5
                spacing 15
                
                for cmd in ["Forward", "Turn Left", "Turn Right"]:
                    textbutton get_command_icon(cmd):
                        action Function(grid.add_command, cmd)
                        style "robot_command_button"
    
    # Область программы
    frame at robot_panel_slide_in(0.24, 80):
        xalign 0.5
        ypos 580
        xsize 900
        ysize 150
        background "#ecf0f1"
        padding (20, 20)
        
        vbox:
            spacing 10
            
            text "Программа (нажмите на команду для удаления):":
                size 20
                color "#2c3e50"
                bold True
                
            # Отображение команд программы
            viewport:
                draggable True
                mousewheel True
                xsize 850
                ysize 80
                clipping True
                
                hbox:
                    spacing 10
                    for i, cmd in enumerate(grid.commands):
                        python:
                            is_current = grid.is_executing and i == grid.execution_index
                            bg_color = "#3498db" if is_current else "#2c3e50"
                        
                        button:
                            background bg_color
                            padding (10, 5)
                            ysize 60
                            action Function(grid.remove_command, i)
                            
                            hbox:
                                spacing 5
                                
                                # Номер команды
                                text "[i+1].":
                                    size 16
                                    color "#fff"
                                    
                                # Иконка команды
                                text get_command_icon(cmd):
                                    size 28
                                    color "#fff"
                                    bold True
                                    
    # Панель управления
    frame at robot_panel_slide_in(0.32, 80):
        xalign 0.5
        ypos 750
        background "transparent"
        
        hbox:
            xalign 0.5
            spacing 30
            
            textbutton "Запустить":
                action [
                    If(
                        grid.execute_full_program(),
                        true=[
                            SetScreenVariable("message", "Успех! Программа работает корректно!"),
                            SetScreenVariable("message_timer", 1),
                            Return(True)
                        ],
                        false=[
                            SetScreenVariable("message", "Ошибка! Программа не достигает цели."),
                            SetScreenVariable("message_timer", 1)
                        ]
                    )
                ]
                style "robot_exam_button"

            textbutton "Пропустить уровень":
                action Return("skip")
                style "robot_exam_button"
                
    if message:
        $ msg_bg = "#27ae60" if "Успех" in message else "#e74c3c"
        frame:
            xalign 0.5
            ypos 820
            background msg_bg
            padding (30, 15)
            
            text message:
                size 28
                color "#fff"
                bold True
                xalign 0.5


# ============================================================================
# ЭКЗАМЕН: КОМПЬЮТЕРНЫЕ СЕТИ
# Мини-игра: соединение каналов данных (пазл с трубами)
# ============================================================================

init python:
    import renpy.store as store
    
    # Таймер на уровень (в секундах)
    LEVEL_TIME_LIMIT = 90.0

    # Направления: 0=Вверх, 1=Вправо, 2=Вниз, 3=Влево
    DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    OPP = {0: 2, 1: 3, 2: 0, 3: 1}

    # Базовые соединения для типов плиток (при повороте 0)
    TILE_BASE = {
        "straight": [0, 2],    # вертикаль
        "corner": [0, 1],      # вверх+вправо
        "tee": [0, 1, 3],      # вверх+вправо+влево
        "cross": [0, 1, 2, 3], # все стороны
        "empty": []
    }

    def rotate_dirs(dirs, rot):
        return [(d + rot) % 4 for d in dirs]

    def tile_connections(tile):
        base = TILE_BASE.get(tile["type"], [])
        return rotate_dirs(base, tile["rot"])

    def rotate_tile(state, r, c):
        """Повернуть плитку по часовой стрелке."""
        tile = state.grid[r][c]
        if tile["type"] == "empty":
            return
        tile["rot"] = (tile["rot"] + 1) % 4
        state.rotations += 1

    def check_connection(state, r, c, direction):
        """
        Проверить, что у плитки есть выход в direction,
        и соседняя плитка имеет встречный выход.
        """
        h = state.size
        w = state.size
        tile = state.grid[r][c]
        conns = tile_connections(tile)
        if direction not in conns:
            return False

        dx, dy = DIRS[direction]
        nr, nc = r + dy, c + dx
        if nr < 0 or nr >= h or nc < 0 or nc >= w:
            return False

        neigh = state.grid[nr][nc]
        neigh_conns = tile_connections(neigh)
        return OPP[direction] in neigh_conns

    def compute_connected(state):
        """Возвращает множество клеток, соединенных со стартом."""
        size = state.size
        sr, sc = state.start

        start_conns = tile_connections(state.grid[sr][sc])
        if not start_conns:
            return set()

        visited = set()
        queue = [(sr, sc)]
        visited.add((sr, sc))

        while queue:
            r, c = queue.pop(0)
            current_conns = tile_connections(state.grid[r][c])
            for d in current_conns:
                dx, dy = DIRS[d]
                nr, nc = r + dy, c + dx
                if nr < 0 or nr >= size or nc < 0 or nc >= size:
                    continue
                if not check_connection(state, r, c, d):
                    continue
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return visited

    def validate_path(state):
        """
        Проверка сети:
        - существует непрерывный путь от START до END
        - соединения считаются валидными только при стыковке двух плиток
        """
        sr, sc = state.start
        er, ec = state.end

        start_conns = tile_connections(state.grid[sr][sc])
        if not start_conns:
            return False, "СТАРТ НЕ ПОДКЛЮЧЕН"

        connected = compute_connected(state)
        if (er, ec) not in connected:
            return False, "ПУТЬ К ФИНАЛУ ПРЕРВАН"

        end_conns = tile_connections(state.grid[er][ec])
        if not end_conns:
            return False, "ФИНАЛ НЕ ПОДКЛЮЧЕН"

        return True, "PING УСПЕШЕН"

    def update_status(state):
        ok, msg = validate_path(state)
        state.status = msg
        state.status_ok = ok
        state.connected = compute_connected(state)
        return None

    def tile_glyph(tile):
        """
        Визуальный символ по текущим соединениям.
        Используем псевдографику.
        """
        conns = sorted(tile_connections(tile))
        s = set(conns)
        if not conns:
            return " "
        if s == {0, 2}:
            return "┃"
        if s == {1, 3}:
            return "━"
        if s == {0, 1}:
            return "┗"
        if s == {1, 2}:
            return "┏"
        if s == {2, 3}:
            return "┓"
        if s == {0, 3}:
            return "┛"
        if s == {0, 1, 3}:
            return "┻"
        if s == {0, 1, 2}:
            return "┣"
        if s == {1, 2, 3}:
            return "┳"
        if s == {0, 2, 3}:
            return "┫"
        return "╋"

    class NetworkPipeState:
        def __init__(self):
            self.level_index = 0
            self.rotations = 0
            self.elapsed = 0.0
            self.status = ""
            self.status_ok = False
            self.connected = set()
            self.grid = []
            self.size = 0
            self.start = (0, 0)
            self.end = (0, 0)
            self.start_dir = 1
            self.end_dir = 3
            self.levels = self._build_levels()

        def _build_levels(self):
            # Уровни: 3 этапа, возрастающая сложность.
            # Каждая плитка: (тип, поворот)
            return [
                {
                    "size": 5,
                    "start": (0, 0),
                    "start_dir": 1,
                    "end": (4, 4),
                    "end_dir": 3,
                    "grid": [
                        [("straight", 1), ("straight", 1), ("straight", 1), ("straight", 1), ("corner", 2)],
                        [("corner", 0), ("tee", 1), ("straight", 0), ("corner", 3), ("straight", 0)],
                        [("straight", 0), ("corner", 0), ("cross", 0), ("corner", 1), ("straight", 0)],
                        [("corner", 1), ("straight", 1), ("tee", 2), ("corner", 2), ("straight", 0)],
                        [("straight", 0), ("corner", 0), ("straight", 0), ("corner", 1), ("corner", 3)]
                    ]
                },
                {
                    "size": 6,
                    "start": (0, 2),
                    "start_dir": 2,
                    "end": (5, 3),
                    "end_dir": 0,
                    "grid": [
                        [("corner", 1), ("straight", 1), ("tee", 0), ("straight", 1), ("corner", 2), ("tee", 3)],
                        [("straight", 0), ("corner", 0), ("straight", 1), ("corner", 3), ("straight", 1), ("corner", 2)],
                        [("tee", 1), ("straight", 0), ("corner", 2), ("cross", 0), ("corner", 0), ("straight", 0)],
                        [("corner", 3), ("straight", 1), ("tee", 2), ("corner", 1), ("straight", 1), ("corner", 0)],
                        [("straight", 0), ("corner", 1), ("straight", 0), ("corner", 2), ("tee", 3), ("straight", 1)],
                        [("corner", 0), ("straight", 1), ("corner", 1), ("straight", 0), ("corner", 3), ("straight", 1)]
                    ]
                },
                {
                    "size": 7,
                    "start": (0, 0),
                    "start_dir": 1,
                    "end": (6, 6),
                    "end_dir": 3,
                    "grid": [
                        [("straight", 1), ("straight", 1), ("straight", 1), ("straight", 1), ("straight", 1), ("straight", 1), ("corner", 2)],
                        [("corner", 0), ("tee", 1), ("straight", 0), ("corner", 3), ("straight", 1), ("tee", 0), ("straight", 0)],
                        [("straight", 0), ("corner", 0), ("cross", 0), ("corner", 1), ("straight", 0), ("corner", 2), ("straight", 0)],
                        [("corner", 1), ("straight", 1), ("tee", 2), ("corner", 2), ("straight", 1), ("corner", 1), ("straight", 0)],
                        [("straight", 0), ("corner", 1), ("straight", 0), ("corner", 2), ("tee", 3), ("straight", 1), ("straight", 0)],
                        [("corner", 0), ("straight", 1), ("corner", 1), ("straight", 0), ("corner", 3), ("straight", 1), ("straight", 0)],
                        [("straight", 0), ("corner", 0), ("straight", 0), ("corner", 1), ("straight", 0), ("corner", 0), ("corner", 3)]
                    ]
                }
            ]

        def load_level(self, idx):
            data = self.levels[idx]
            self.size = data["size"]
            self.start = data["start"]
            self.end = data["end"]
            self.start_dir = data["start_dir"]
            self.end_dir = data["end_dir"]
            self.rotations = 0
            self.elapsed = 0.0
            self.status = ""
            self.status_ok = False
            self.connected = set()

            # Копируем сетку и случайно вращаем (создаем динамическую задачу)
            import random
            self.grid = []
            for row in data["grid"]:
                new_row = []
                for t, r in row:
                    rot = (r + random.randint(0, 3)) % 4
                    new_row.append({"type": t, "rot": rot})
                self.grid.append(new_row)

    def score_for_level(level_idx, rotations, elapsed):
        # Базовые очки за уровень (более справедливо)
        base = [40, 35, 35][level_idx]
        # Штрафы только после "разумных" порогов
        rot_pen = max(0, rotations - 10) * 0.4
        time_pen = max(0, elapsed - 30.0) * 0.15
        # Минимум за успешно пройденный уровень
        return max(20, int(base - rot_pen - time_pen))


label run_exam_networks:
    """
    Экзамен: Компьютерные сети.
    Реализован как визуальный пазл соединения каналов данных.
    """
    python:
        network_pipes = NetworkPipeState()

    "Экзамен: Компьютерные сети"
    "Задача: восстановите сеть, соединяя каналы данных."
    "Вам предстоит пройти 3 уровня возрастающей сложности."

    python:
        total_score = 0
        completed = 0
        for i in range(3):
            network_pipes.level_index = i
            network_pipes.load_level(i)
            _window_hide()
            result = renpy.call_screen("network_pipes_screen", network_pipes)
            if result is True:
                completed += 1
                total_score += score_for_level(i, network_pipes.rotations, network_pipes.elapsed)
            elif result == "skip":
                total_score = 0
                renpy.say(None, "Экзамен пропущен. (0 баллов)")
                break
            elif result == "timeout":
                total_score = 0
                renpy.say(None, "Время вышло! Сеть не восстановлена. (0 баллов)")
                break
            else:
                # Если игрок вышел, фиксируем текущий результат
                break

    python:
        total_score = int(min(100, max(0, total_score)))

    if total_score >= 90:
        "Превосходно! Сеть работает идеально."
    elif total_score >= 70:
        "Хорошо! Каналы восстановлены."
    elif total_score >= 50:
        "Удовлетворительно. Связь нестабильна, но есть."
    else:
        "Сеть не восстановлена. Требуется повторная настройка."

    $ store.exam_grades["networks"] = total_score
    return total_score


screen network_pipes_screen(state):
    default message = ""
    default msg_color = "#f1faee"

    # Таймер
    timer 0.1 repeat True action [
        SetField(state, "elapsed", state.elapsed + 0.1),
        If(state.elapsed >= LEVEL_TIME_LIMIT, Return("timeout"))
    ]
    timer 0.2 repeat True action Function(update_status, state)

    add "#0d1b2a"

    # Заголовок
    frame:
        xalign 0.5
        ypos 20
        background "#1b263b"
        padding (30, 15)

        vbox:
            spacing 8
            text "КОМПЬЮТЕРНЫЕ СЕТИ — УРОВЕНЬ [state.level_index + 1]/3":
                size 36
                color "#e0e1dd"
                bold True
                xalign 0.5
            
            python:
                time_left = max(0, LEVEL_TIME_LIMIT - state.elapsed)
                time_color = "#e76f51" if time_left < 10 else "#778da9"
                
            text "Осталось времени: [time_left:.1f]с | Повороты: [state.rotations]":
                size 24
                color time_color
                xalign 0.5

    # Кнопка пропуска
    textbutton "Пропустить экзамен":
        align (0.95, 0.05)
        action Return("skip")
        text_size 18
        text_color "#fff"
        background "#e76f51"
        padding (10, 5)

    # Игровая сетка
    frame:
        xalign 0.5
        yalign 0.5
        background "#1b263b"
        padding (20, 20)

        grid state.size state.size:
            spacing 6
            for r in range(state.size):
                for c in range(state.size):
                    python:
                        tile = state.grid[r][c]
                        glyph = tile_glyph(tile)
                        is_start = (r, c) == state.start
                        is_end = (r, c) == state.end
                        is_connected = (r, c) in state.connected
                        bg = "#415a77"
                        if is_start:
                            bg = "#2a9d8f"
                        elif is_end:
                            bg = "#e76f51"
                        elif is_connected:
                            bg = "#5c7ea6"
                    button:
                        xsize 70
                        ysize 70
                        background bg
                        action [
                            Function(rotate_tile, state, r, c),
                            SetScreenVariable("message", ""),
                            SetScreenVariable("msg_color", "#f1faee")
                        ]
                        text glyph:
                            size 40
                            color "#ffffff"
                            xalign 0.5
                            yalign 0.5
                            bold True
                        if is_start:
                            text "START":
                                size 12
                                color "#0d1b2a"
                                xalign 0.5
                                yalign 1.0
                        if is_end:
                            text "END":
                                size 12
                                color "#0d1b2a"
                                xalign 0.5
                                yalign 1.0

    # Панель управления
    frame:
        xalign 0.5
        yalign 0.9
        background "#1b263b"
        padding (30, 15)

        hbox:
            spacing 20
            textbutton "ПРОВЕРИТЬ СЕТЬ":
                xsize 260
                ysize 60
                background "#457b9d"
                hover_background "#3d6f8f"
                text_size 24
                text_color "#ffffff"
                action [
                    Function(update_status, state),
                    SetScreenVariable("message", state.status),
                    SetScreenVariable("msg_color", "#2a9d8f" if state.status_ok else "#e76f51")
                ]

            textbutton "ОТПРАВИТЬ PING":
                xsize 260
                ysize 60
                background "#2a9d8f"
                hover_background "#21867a"
                text_size 24
                text_color "#ffffff"
                sensitive state.status_ok
                action [
                    Function(update_status, state),
                    If(
                        state.status_ok,
                        true=[
                            SetScreenVariable("message", state.status),
                            SetScreenVariable("msg_color", "#2a9d8f"),
                            Return(True)
                        ],
                        false=[
                            SetScreenVariable("message", state.status),
                            SetScreenVariable("msg_color", "#e76f51")
                        ]
                    )
                ]

            textbutton "СБРОС УРОВНЯ":
                xsize 220
                ysize 60
                background "#577590"
                hover_background "#4a647f"
                text_size 22
                text_color "#ffffff"
                action [
                    Function(state.load_level, state.level_index),
                    SetScreenVariable("message", ""),
                    SetScreenVariable("msg_color", "#f1faee")
                ]

            textbutton "ВЫЙТИ":
                xsize 140
                ysize 60
                background "#bc4749"
                hover_background "#a63d40"
                text_size 22
                text_color "#ffffff"
                action Return(False)

    # Сообщение
    if message:
        frame:
            xalign 0.5
            yalign 0.82
            background "#0d1b2a"
            padding (20, 10)
            text message:
                size 28
                color msg_color
                bold True
                xalign 0.5

    # Индикатор готовности сети
    if state.status_ok:
        text "СЕТЬ ГОТОВА — МОЖНО ОТПРАВЛЯТЬ PING":
            xalign 0.5
            yalign 0.78
            size 22
            color "#2a9d8f"
    else:
        text "СЕТЬ НЕ ГОТОВА":
            xalign 0.5
            yalign 0.78
            size 22
            color "#e76f51"

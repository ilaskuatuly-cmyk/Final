init python:
    import renpy.store as store

    # === GENERAL EXAM CONTROLLER ===
    def run_exam(subject, resume_music=None):
        """
        Executes a multi-phase exam and returns the total score (0-100).
        """
        total_score = 0
        
        renpy.say(None, "Экзамен начинается. У вас 100 баллов на кону.")
        _window_hide()
        
        if subject == "programming":
            renpy.music.play("audio/Soundtracks/Programming.mp3", channel="music", fadein=1.0)
            total_score = run_minigame_programming()
            
        elif subject == "psychology":
            renpy.music.play("audio/Soundtracks/Psychology.mp3", channel="music", fadein=1.0)
            total_score = run_minigame_psychology()

        elif subject == "cryptography":
            renpy.music.play("audio/Soundtracks/Crypto.mp3", channel="music", fadein=1.0)
            total_score = run_phase_cryptography_1()

        elif subject == "math_analysis":
            renpy.music.play("audio/Soundtracks/Math.mp3", channel="music", fadein=1.0)
            renpy.call("run_exam_math")
            total_score = store._return
              
        elif subject == "english":
            renpy.music.play("audio/Soundtracks/English.mp3", channel="music", fadein=1.0)
            total_score = run_minigame_english()

        elif subject == "networks":
            renpy.music.play("audio/Soundtracks/Network.mp3", channel="music", fadein=1.0)
            renpy.call("run_exam_networks")
            total_score = store._return

        # Stop exam music after the exam finishes.
        renpy.music.stop(channel="music", fadeout=0.5)
        if resume_music:
            renpy.music.play(resume_music, channel="music", fadein=1.0)

        # Clamp and Save
        final_score = int(min(100, max(0, total_score)))
        store.exam_grades[subject] = final_score
        
        # Feedback (без отображения баллов)
        renpy.say(None, "Экзамен завершен.")
        
        return final_score

    # ==========================================
    # SUBJECT 1: INTRODUCTION TO PROGRAMMING
    # ==========================================
    
    # Phase 1: Syntax Error Hunt (25 pts)
    def run_phase_programming_1():
        renpy.say(None, "Фаза 1: Найдите синтаксическую ошибку.")
        # Code with an error
        code_lines = [
            "def calculate_area(r):",
            "    pi = 3.14",
            "    return pi * r ^ 2" # Error: ^ is XOR in python, usually **
        ]
        # Valid indices (0,1,2). Correct answer is index 2.
        
        if store.helped_ayan:
            renpy.say(None, "Аян напоминал: 'В Питоне степень это две звездочки'.")
            
        result = renpy.call_screen("exam_click_error_screen", 
                                   title="ПРОГРАММИРОВАНИЕ - ФАЗА 1/4",
                                   code_lines=code_lines)
                                   
        if result == 2:
            return 25
        return 0

    # Phase 2: Variable Logic (25 pts)
    def run_phase_programming_2():
        renpy.say(None, "Фаза 2: Логика переменных. Чему равен X?")
        
        # x = 10
        # for i in range(3):
        #    x += i
        # return x
        # 10 + 0 + 1 + 2 = 13.
        
        result = renpy.call_screen("exam_input_screen", 
                                   title="ПРОГРАММИРОВАНИЕ - ФАЗА 2/4",
                                   prompt="x = 10\nfor i in range(3):\n    x += i\nprint(x)")
                                   
        if result.strip() == "13":
            return 25
        return 0

    # Phase 3: Code Ordering (25 pts)
    def run_phase_programming_3():
        renpy.say(None, "Фаза 3: Восстановите алгоритм сортировки.")
        
        lines = [
            "for i in range(len(arr)):",
            "    for j in range(len(arr)-1):",
            "        if arr[j] > arr[j+1]:",
            "            arr[j], arr[j+1] = arr[j+1], arr[j]"
        ]
        # Scramble them for display? The screen usually takes a list and lets user order them.
        # We will pass them in scrambled order.
        scrambled = [lines[2], lines[0], lines[3], lines[1]]
        correct_indices = [1, 3, 0, 2] # Map back to scrambled
        
        result = renpy.call_screen("exam_ordering_screen", 
                                   title="ПРОГРАММИРОВАНИЕ - ФАЗА 3/4",
                                   items=scrambled)
                                   
        if result == correct_indices:
            return 25
        return 5 # Pity points

    # Phase 4: Big O Optimization (25 pts)
    def run_phase_programming_4():
        renpy.say(None, "Фаза 4: Выберите оптимальное решение (O(n)).")
        
        options = [
            "Двойной цикл (Nested Loops)",
            "Хеш-таблица (Hash Map)",
            "Рекурсия без мемоизации"
        ]
        
        result = renpy.call_screen("exam_choice_screen", 
                                   title="ПРОГРАММИРОВАНИЕ - ФАЗА 4/4",
                                   question="Какая структура данных ускорит поиск дубликатов?",
                                   options=options)
                                   
        if result == 1:
            return 25
        return 0

    # ==========================================
    # SUBJECT 2: PSYCHOLOGY
    # ==========================================

    # Phase 1: Micro-expressions (30 pts)
    def run_phase_psychology_1():
        renpy.say(None, "Фаза 1: Анализ эмоций.")
        
        desc = "Пациент быстро моргает, уголки губ опущены, руки скрещены."
        # Fear? Sadness? Defensive?
        
        tags = ["Гнев", "Печаль", "Защита", "Радость", "Тревога"]
        correct = {"Печаль", "Защита", "Тревога"}
        
        if store.trusted_diana:
            renpy.say(None, "Диана советовала обращать внимание на руки.")
        
        result_tags = renpy.call_screen("exam_multiselect_screen",
                                        title="ПСИХОЛОГИЯ - ФАЗА 1/3",
                                        prompt=desc,
                                        options=tags)
                                        
        # Scoring: 10 pts per correct tag, -5 per wrong
        score = 0
        for t in result_tags:
            if t in correct:
                score += 10
            else:
                score -= 5
        return max(0, min(30, score))

    # Phase 2: Dialogue Analysis (40 pts)
    def run_phase_psychology_2():
        renpy.say(None, "Фаза 2: Реакция терапевта.")
        
        q = "Клиент: 'Я ничтожество, у меня ничего не выходит!'"
        opts = [
            "Вам просто нужно отдохнуть.", # Dismissive
            "Звучит так, будто вы чувствуете бессилие. Расскажите подробнее.", # Active listening (Correct)
            "Давайте посмотрим на ваши успехи." # Logic (Too early)
        ]
        
        result = renpy.call_screen("exam_choice_screen",
                                   title="ПСИХОЛОГИЯ - ФАЗА 2/3",
                                   question=q,
                                   options=opts)
        
        if result == 1:
            return 40
        elif result == 2:
            return 20
        return 0

    # Phase 3: Diagnosis (30 pts)
    def run_phase_psychology_3():
        renpy.say(None, "Фаза 3: Предварительный диагноз.")
        
        # Drag and drop symptoms? Or just a choice?
        # Let's use multi-select again but with stricter logic.
        
        desc = "Симптомы: Потеря интереса, бессонница, потеря веса, чувство вины > 2 недель."
        opts = ["Шизофрения", "Большое депрессивное расстройство", "Биполярное расстройство", "ГТР"]
        
        result = renpy.call_screen("exam_choice_screen",
                                   title="ПСИХОЛОГИЯ - ФАЗА 3/3",
                                   question=desc,
                                   options=opts)
                                   
        if result == 1:
            return 30
        return 0

    # ==========================================
    # SUBJECT 3: CRYPTOGRAPHY (LOCKPICKING)
    # ==========================================

    def run_phase_cryptography_1():
        # This function now runs the WHOLE exam logic because it's a unified minigame loop
        # We will return the TOTAL score here and skip phases 2 and 3 in the main controller?
        # Or we split the locks across phases?
        # The user said "5 locks".
        # Let's make this function run all 5 locks and return the total score.
        # We will adjust the main controller to only call this one.
        
        renpy.say(None, "Экзамен по Криптографии: Практика взлома.")
        renpy.say(None, "Вам нужно вскрыть 5 замков. У вас ограниченное количество отмычек.")
        
        store.current_lockpicks = 8
        if store.bonded_timur:
            store.current_lockpicks += 1
            renpy.say(None, "Тимур дал тебе запасную отмычку. (+1)")
            
        score = 0
        locks_count = 5
        difficulties = [20, 18, 15, 12, 10] # Decreasing number = Harder in the Lock class logic?
        # Looking at valid code: difficulty is "range of error". So smaller is harder.
        # Original code: 20 (Easy), 4 (Hard).
        
        for i in range(locks_count):
            renpy.say(None, f"Замок {i+1}/5.")
            
            # Difficulty increases (number gets smaller)
            diff = difficulties[i]
            
            success = renpy.call_screen("lockpicking_game", difficulty=diff)
            
            if success is True:
                score += 20
                renpy.say(None, "Замок открыт!")
            elif success == "skip":
                return 0
            else:
                renpy.say(None, "Не удалось открыть замок.")
                if store.current_lockpicks <= 0:
                    renpy.say(None, "Отмычки закончились. Экзамен завершен.")
                    break
                    
        return score

    # Legacy placeholders if the main controller calls them
    def run_phase_cryptography_2():
        return 0
        
    def run_phase_cryptography_3():
        return 0

    # ==========================================
    # SUBJECT 4: MATH ANALYSIS
    # ==========================================

    # Phase 1: Limits (30 pts)
    def run_phase_math_1():
        renpy.say(None, "Фаза 1: Пределы.")
        
        # lim x->inf (2x^2 + 1) / (x^2) = 2.
        
        result = renpy.call_screen("exam_adjuster_screen",
                                   title="МАТ. АНАЛИЗ - ФАЗА 1/3",
                                   prompt="lim (2x^2 + 1) / (x^2) при x -> inf",
                                   initial_value=0,
                                   min_val=0,
                                   max_val=10)
                                   
        if result == 2:
            return 30
        return 0

    # Phase 2: Derivative Chain (30 pts)
    def run_phase_math_2():
        renpy.say(None, "Фаза 2: Производная (x^3 + 5x).")
        # 3x^2 + 5
        parts = ["3x^2", "+", "5"]
        scrambled = ["5", "3x^2", "+"]
        correct_indices = [1, 2, 0]
        
        result = renpy.call_screen("exam_ordering_screen",
                                   title="МАТ. АНАЛИЗ - ФАЗА 2/3",
                                   items=scrambled)
                                   
        if result == correct_indices:
            return 30
        return 5

    # Phase 3: Integral (40 pts)
    def run_phase_math_3():
        renpy.say(None, "Фаза 3: Интеграл 2x dx.")
        
        options = ["x^2 + C", "2x^2 + C", "x + C"]
        result = renpy.call_screen("exam_choice_screen",
                                   title="МАТ. АНАЛИЗ - ФАЗА 3/3",
                                   question="Чему равен интеграл?",
                                   options=options)
                                   
        if result == 0:
            return 40
        return 0

    # ==========================================
    # SUBJECT 5: ENGLISH LANGUAGE
    # ==========================================

    # Phase 1: Comprehension (30 pts)
    def run_phase_english_1():
        renpy.say(None, "Phase 1: Reading Comprehension.")
        renpy.say(None, "Text: 'The network latency caused packet loss.'")
        
        q = "What caused the issue?"
        opts = ["The packet size", "The latency", "The user"]
        
        result = renpy.call_screen("exam_choice_screen",
                                   title="ENGLISH - PHASE 1/3",
                                   question=q,
                                   options=opts)
                                   
        if result == 1:
            return 30
        return 0
        
    # Phase 2: Word Order (30 pts)
    def run_phase_english_2():
        renpy.say(None, "Phase 2: Sentence Construction.")
        # "I have never been to London"
        items = ["never", "I", "to", "have", "London", "been"]
        correct_indices = [1, 3, 0, 5, 2, 4]
        
        if store.practiced_alina:
            renpy.say(None, "Alina's voice: 'Present Perfect order: Subject + Have + Participle'.")
            
        result = renpy.call_screen("exam_ordering_screen",
                                   title="ENGLISH - PHASE 2/3",
                                   items=items)
                                   
        if result == correct_indices:
             return 30
        return 5

    # Phase 3: Context (40 pts)
    def run_phase_english_3():
        renpy.say(None, "Phase 3: Formal Reply.")
        
        q = "Interviewer: 'Why should we hire you?'"
        opts = [
            "Because I'm the best.", 
            "I believe my skills in Python fit the role perfectly.", # Correct
            "I need money."
        ]
        
        result = renpy.call_screen("exam_choice_screen",
                                   title="ENGLISH - PHASE 3/3",
                                   question=q,
                                   options=opts)
                                   
        if result == 1:
            return 40
        return 0

    # ==========================================
    # SUBJECT 6: COMPUTER NETWORKS
    # ==========================================

    # Phase 1: Topology (30 pts)
    def run_phase_networks_1():
        renpy.say(None, "Фаза 1: Топология 'Звезда'.")
        
        q = "Какой элемент является центральным?"
        opts = ["Switch (Коммутатор)", "Server", "Client"]
        
        result = renpy.call_screen("exam_choice_screen",
                                   title="СЕТИ - ФАЗА 1/3",
                                   question=q,
                                   options=opts)
                                   
        if result == 0:
            return 30
        return 0

    # Phase 2: OSI Model (30 pts)
    def run_phase_networks_2():
        renpy.say(None, "Фаза 2: Уровни модели OSI (снизу вверх).")
        
        items = ["Network (Сетевой)", "Physical (Физический)", "Transport (Транспортный)"]
        # Correct: Physical -> Network -> Transport? No, Data Link is missing.
        # Let's assume subsets. Physical is L1. Network is L3. Transport is L4.
        # Order: Physical -> Network -> Transport.
        
        scrambled = ["Network (Сетевой)", "Transport (Транспортный)", "Physical (Физический)"]
        correct_indices = [2, 0, 1]
        
        result = renpy.call_screen("exam_ordering_screen",
                                   title="СЕТИ - ФАЗА 2/3",
                                   items=scrambled)
                                   
        if result == correct_indices:
            return 30
        return 5

    # Phase 3: Packet Trace (40 pts)
    def run_phase_networks_3():
        renpy.say(None, "Фаза 3: Поиск ошибки. Ping не проходит.")
        
        # Scenario
        q = "PC1 (192.168.1.5) -> Router (192.168.2.1). Mask /24. В чем проблема?"
        opts = [
            "Разные подсети, шлюз настроен неверно.", 
            "Кабель поврежден.", 
            "DNS не работает."
        ]
        
        result = renpy.call_screen("exam_choice_screen",
                                   title="СЕТИ - ФАЗА 3/3",
                                   question=q,
                                   options=opts)
                                   
        if result == 0:
            return 40
        return 0

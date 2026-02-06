# -*- coding: utf-8 -*-
init python:

    # Psychology Minigame
    # Drag emotions to the correct patient statement.

    def psycho_check_drag(drags, drop):
        if not drop:
            return
        
        emotion = drags[0].drag_name
        target = drop.drag_name
        
        # Mapping logic stored in screen variable or global?
        # Let's pass it via store for simplicity or check string equality if we name them cleverly.
        
        # If target is "Target_Anxiety" and emotion is "Anxiety" -> Match.
        
        if emotion in target:
            return True
        return False

screen minigame_psychology_screen(scenario_text, correct_pairs, options):
    # correct_pairs: dict of {target_id: correct_emotion_name}
    # options: list of emotion names to drag
    
    default solved_count = 0
    default target_count = len(correct_pairs)
    
    add "#2c3e50"
    
    vbox:
        xalign 0.5
        yalign 0.05
        text "Проанализируйте пациента:" color "#fff" size 40 bold True font "DejaVuSans.ttf"
        text scenario_text color "#bdc3c7" size 28 italic True font "DejaVuSans.ttf"
    
    # Drag Group
    draggroup:
        # Drop Zones (Representing aspects of the patient)
        # We display them as boxes
        
        for i, (target_id, correct_emo) in enumerate(correct_pairs.items()):
            drag:
                drag_name target_id
                droppable True
                draggable False
                xpos 400 + (i*400)
                ypos 400
                frame:
                    xsize 300
                    ysize 200
                    background "#34495e"
                    text "Аспект: " + target_id color "#fff" align (0.5, 0.1) font "DejaVuSans.ttf"
                    text "(Перетащите сюда эмоцию)" color "#7f8c8d" align (0.5, 0.5) size 20 font "DejaVuSans.ttf"

                dropped (lambda d, drop, t=target_id, c=correct_emo: psycho_dropped(d, drop, c))

        # Draggable Emotions (Options)
        for i, opt in enumerate(options):
            drag:
                drag_name opt
                droppable False
                draggable True
                xpos 200 + (i*200)
                ypos 700
                frame:
                    background "#e67e22"
                    padding (10, 10)
                    text opt color "#fff" bold True font "DejaVuSans.ttf"

    # Helper to handle drop (Since lambda in screen is tricky with returns)
    # Actually, standard drag/drop in RenPy is event based.
    # Let's use a simplified "Click to assign" if drag is too complex for this context, 
    # but Drag is requested.
    # Using a simplified approach: 
    # The drag callback sets a variable.

    textbutton "Проверить":
        align (0.9, 0.9)
        style "exam_button"
        text_style "exam_button_text"
        action Return(solved_count)

    # Кнопка пропуска
    textbutton "Пропустить фазу":
        align (0.95, 0.05)
        action Return("skip")
        text_size 16
        text_color "#bdc3c7"
        text_hover_color "#fff"

init python:
    def psycho_dropped(drop_target, dragged_items, correct_answer):
        if dragged_items:
            # dragged_items is a list of Drag objects, get the first one
            if dragged_items[0].drag_name == correct_answer:
                store.psycho_session_score += 1
            else:
                store.psycho_session_score -= 1  # Penalty

    store.psycho_session_score = 0

    def run_minigame_psychology():
        total = 0
        renpy.say(None, "Психология: Диагностика.")
        _window_hide()
        
        # Scenario 1
        store.psycho_session_score = 0
        s1 = "Пациент постоянно шутит, избегает зрительного контакта."
        pairs1 = {"Лицо": "Страх", "Речь": "Защита"}
        opts1 = ["Радость", "Страх", "Защита", "Гнев"]
        
        res = renpy.call_screen("minigame_psychology_screen", 
                          scenario_text=s1, 
                          correct_pairs=pairs1, 
                          options=opts1)
        
        if res == "skip": return 0
                          
        # Score calculation
        # If score >= 2 (max), full points.
        if store.psycho_session_score >= 2: total += 35
        elif store.psycho_session_score == 1: total += 15

        # Scenario 2
        store.psycho_session_score = 0
        s2 = "Агрессивно реагирует на вопросы о матери."
        pairs2 = {"Реакция": "Проекция", "Тон": "Гнев"}
        opts2 = ["Отрицание", "Проекция", "Гнев", "Печаль"]
        
        res = renpy.call_screen("minigame_psychology_screen",
                          scenario_text=s2,
                          correct_pairs=pairs2,
                          options=opts2)
                          
        if res == "skip": return 0
                          
        if store.psycho_session_score >= 2: total += 35
        elif store.psycho_session_score == 1: total += 15
        
        # Scenario 3 (Therapy choices - easier, just choice)
        renpy.say(None, "Выберите терапию.")
        res = renpy.call_screen("exam_choice_screen", 
                                title="Терапия", 
                                question="Клиент плачет. Ваши действия?", 
                                options=["Обнять", "Молчать (Поддержка)", "Сменить тему"])
        if res == 1: total += 30
        elif res == "skip": return 0
        
        return total

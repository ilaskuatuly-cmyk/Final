# English Minigame: Speed Improv
# Timer counts down. Options disappear? Or just fail if 0.

screen minigame_english_improv(prompt_text, options, correct_idx, time_limit=5.0):
    default time_left = time_limit
    
    timer 0.1 repeat True action [
        SetScreenVariable("time_left", time_left - 0.1),
        If(time_left <= 0, Return(-1)) # -1 = Timeout
    ]
    
    add "#2c3e50"
    
    # Timer Bar
    bar:
        value time_left
        range time_limit
        xalign 0.5
        yalign 0.1
        xsize 800
        ysize 20
        left_bar Frame("gui/bar/left.png", 0, 0) # Default renpy bars if available, or solid color
        right_bar Solid("#e74c3c")
        
    text "[time_left:.1f] s" xalign 0.5 yalign 0.05 color "#fff" size 40

    vbox:
        align (0.5, 0.4)
        spacing 30
        text prompt_text size 35 color "#fff" italic True xalign 0.5
        
        for i, opt in enumerate(options):
            textbutton opt:
                xalign 0.5
                style "exam_button"
                action Return(i)

    # Кнопка пропуска
    textbutton "Пропустить фазу":
        align (0.95, 0.05)
        action Return("skip")
        text_size 16
        text_color "#bdc3c7"
        text_hover_color "#fff"

init python:
    import renpy.store as store
    def run_minigame_english():
        score = 0
        renpy.say(None, "English: Keep the Flow! (Отвечайте быстро!)")
        
        # Усложнение: базовое время меньше, помощь Алины дает +3 сек к каждому вопросу
        bonus_time = 3.0 if store.practiced_alina else 0.0
        
        # Round 1
        _window_hide()
        res1 = renpy.call_screen("minigame_english_improv", 
                                 prompt_text="Teacher: 'Could you clarify why you arrived after the bell?'",
                                 options=["I overslept.", "My dog ate my homework.", "Traffic was terrible."],
                                 correct_idx=2, # Traffic is a valid excuse? Or overslept? Let's say all are okay but 
                                 # Context: Formal? "Traffic" is best.
                                 time_limit=7.0 + bonus_time)
                                 
        if res1 == "skip": return 0
        elif res1 == 2: score += 30
        elif res1 != -1: score += 15 # Consolation for any answer
        else: renpy.say(None, "Time out! (-0)")
        
        # Round 2
        res2 = renpy.call_screen("minigame_english_improv",
                                 prompt_text="Interviewer: 'Describe a weakness and how you manage it.'",
                                 options=["I work too hard.", "I am lazy.", "I hate people."],
                                 correct_idx=0,
                                 time_limit=7 + bonus_time)
                                 
        if res2 == "skip": return 0
        elif res2 == 0: score += 30
        elif res2 != -1: score += 10
        
        # Round 3
        res3 = renpy.call_screen("minigame_english_improv",
                                 prompt_text="Tourist: 'Excuse me, could you tell me how to get to the station?'",
                                 options=["Go left.", "I don't know.", "It is over there, sir."],
                                 correct_idx=2, # Polite
                                 time_limit=7 + bonus_time)
                                 
        if res3 == "skip": return 0
        elif res3 == 2: score += 40
        elif res3 != -1: score += 20
        
        return score

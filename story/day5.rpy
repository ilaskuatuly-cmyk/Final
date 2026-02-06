label day5:
    scene bg room
    
    show screen day_indicator("День 5")
    
    "Пятница. Финал."
    "Последний рывок. Английский язык и Компьютерные Сети."
    "Если сдам их — свобода."
    
    scene bg hallway
    "В коридоре подозрительно тихо. Либо все уже сдали, либо..."
    
    $ run_exam("english")
    
    "Английский прошел как во сне. 'London is the capital of Great Britain', да?"
    "Надеюсь, фаза с контекстом меня не подвела."
    
    "И наконец... Сети. Самый страшный предмет семестра."
    
    $ run_exam("networks")
    
    scene bg room
    "Всё. Кончилось."
    "Осталось только дождаться результатов."
    
    jump endings

label endings:
    scene bg room
    
    # Расчет результатов
    $ final_gpa = calculate_gpa()
    $ total_relationships = ayan_relationship + diana_relationship + timur_relationship + alina_relationship
    
    "Твой телефон вибрирует. Пришло уведомление из деканата."
    
    # Экран результатов (Таблица)
    call screen final_results_screen(final_gpa)
    
    # Логика концовок (GPA 4.0 scale + Relationships)
    
    # 1. High GPA + Social (Balanced)
    if final_gpa >= 3.5 and total_relationships >= 3:
        jump ending_balanced
        
    # 2. High GPA + Loner (Academic)
    elif final_gpa >= 3.5:
        jump ending_academic_loner
        
    # 3. Low GPA + Social (Social Failure/Party)
    elif final_gpa < 2.5 and total_relationships >= 4:
        jump ending_social_failure
        
    # 4. Burnout (Average/Low GPA + Low social)
    else:
        jump ending_burnout

label ending_balanced:
    scene bg cafeteria
    "Концовка: Золотая Середина"
    "Ты смотришь на свой средний балл: [final_gpa]. Отлично."
    "Вокруг сидят друзья. Аян, Диана, Тимур, Алина."
    "Ты смог не только выучить, но и не потерять себя."
    return

label ending_academic_loner:
    scene bg room
    "Концовка: Одинокий Волк"
    "Ты открываешь зачетку. Одни 'А'. Средний балл: [final_gpa]."
    "Ты лучший на потоке."
    "В комнате тихо. Телефон молчит. Никто не зовет праздновать."
    "Зато ты победил."
    return

label ending_burnout:
    scene bg room
    "Концовка: Выгорание"
    "Сессия закрыта. Балл: [final_gpa]. Не отлично, не ужасно."
    "Но внутри — пустота. Ты просто хочешь спать следующие три дня."
    "Может, стоило больше гулять? Или больше учить? Уже не важно."
    return

label ending_social_failure:
    scene bg park
    "Концовка: Душа Компании (но на пересдачу)"
    "Балл [final_gpa] вряд ли порадует родителей."
    "Но друзья тащат тебя в бар."
    "Тимур: 'Оценки — это цифры. А дружба — это протокол без потерь пакетов'."
    "По крайней мере, тебе весело."
    return

screen final_results_screen(gpa):
    modal True
    add "#2c3e50"
    
    frame:
        xalign 0.5
        yalign 0.5
        padding (50, 50)
        background "#34495e"
        
        vbox:
            spacing 20
            text "ЭКЗАМЕНАЦИОННАЯ ВЕДОМОСТЬ" size 50 xalign 0.5 bold True color "#ecf0f1"
            
            null height 20
            
            grid 3 7:
                spacing 15
                xalign 0.5
                
                # Headers
                text "Предмет" color "#bdc3c7" bold True size 30
                text "Баллы" color "#bdc3c7" bold True size 30
                text "Оценка" color "#bdc3c7" bold True size 30
                
                # Rows
                text "Программирование" color "#fff" size 25
                text "[exam_grades['programming']]" color "#fff" size 25
                text "[get_letter_grade(exam_grades['programming'])]" color "#f1c40f" bold True size 25
                
                text "Психология" color "#fff" size 25
                text "[exam_grades['psychology']]" color "#fff" size 25
                text "[get_letter_grade(exam_grades['psychology'])]" color "#f1c40f" bold True size 25
                
                text "Криптография" color "#fff" size 25
                text "[exam_grades['cryptography']]" color "#fff" size 25
                text "[get_letter_grade(exam_grades['cryptography'])]" color "#f1c40f" bold True size 25
                
                text "Мат. Анализ" color "#fff" size 25
                text "[exam_grades['math_analysis']]" color "#fff" size 25
                text "[get_letter_grade(exam_grades['math_analysis'])]" color "#f1c40f" bold True size 25
                
                text "Английский" color "#fff" size 25
                text "[exam_grades['english']]" color "#fff" size 25
                text "[get_letter_grade(exam_grades['english'])]" color "#f1c40f" bold True size 25
                
                text "Компьютерные Сети" color "#fff" size 25
                text "[exam_grades['networks']]" color "#fff" size 25
                text "[get_letter_grade(exam_grades['networks'])]" color "#f1c40f" bold True size 25
            
            null height 30
            text "ИТОГОВЫЙ GPA: [gpa]" size 60 xalign 0.5 color "#e74c3c" bold True outlines [(2, "#000", 0, 0)]
            
            textbutton "Завершить семестр":
                xalign 0.5
                style "exam_button"
                text_style "exam_button_text"
                action Return()

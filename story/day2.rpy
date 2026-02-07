label day2:
    scene bg room
    
    show screen day_indicator("День 2")
    
    "День 2. Передышка."
    "Сегодня нет экзаменов, но атмосфера все равно напряженная."
    
    "Нужно решить, как провести этот день. Подготовка важна, но связи — еще важнее."
    
    menu:
        "Пойти в библиотеку (Криптография).":
            jump day2_library
        
        "Прогуляться в парке (Английский).":
            jump day2_park
            
        "Остаться в общежитии и зубрить (Матан).":
            jump day2_dorm

label day2_library:
    scene bg library
    "В библиотеке пахнет старой бумагой и пылью."
    "Тимур сидит в углу, обложившись книгами про 'Энигму'."
    
    show timur at center
    
    "Ты подходишь к нему. Он даже не поднимает глаз."
    
    menu:
        "Спросить про шифр Виженера.":
            timur "Слишком просто. Лучше посмотри на роторные машины."
            "Его глаза загораются. Он начинает рассказывать про криптоанализ."
            $ bonded_timur = True
            $ timur_relationship += 2
            "Ты узнаешь много нового про сдвиги шифров."
            
        "Просто сесть рядом и учить.":
            "Вы сидите в тишине. Иногда это лучше пустого трепа."
            $ timur_relationship += 1
            
    hide timur
    jump day2_evening

label day2_park:
    scene bg os
    
    "Алина сидит на лавочке и слушает подкаст на английском."
    
    show alina at center
    
    alina "Hi! Do you mind joining me?"
    
    menu:
        "Sure, let's practice speaking.":
            "Вы проводите час, обсуждая погоду, политику и экзамены на английском."
            $ practiced_alina = True
            $ alina_relationship += 2
            alina "Your grammar is getting better!"
            
        "I'm actually busy right now.":
            alina "Oh, okay. See you later."
            
    hide alina
    jump day2_evening

label day2_dorm:
    scene bg room
    "Ты решаешь, что социализация — это трата времени."
    "Ты открываешь учебник по Матанализу."
    "Пределы, производные, интегралы... Голова кругом."
    
    "Зато ты чувствуешь себя увереннее в формулах."
    $ studied_matan = True
    
    jump day2_evening

label day2_evening:
    scene bg room
    "Вечер наступил слишком быстро."
    "Завтра Криптография и Математический Анализ."
    "Самые сложные предметы."
    
    jump day3

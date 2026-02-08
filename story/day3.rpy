label day3:
    scene bg room
    
    
    show screen day_indicator("День 3")
    
    "Среда.Самые сложные предметы сегодня."
    "Криптография и Математический Анализ. Звучит как музыка... похоронная."
    
    scene bg hallway
    play music "audio/Soundtracks/hall.mp3" fadein 1.0
    
    show timur at center
    timur "Расслабься, главное не сбиться с алгоритма. Будь повнимательнее."
    
    "Хоть Тимур и лучший в крипте, он все равно готовился к ней как не в себя."
    
    menu:
        "Ты прав. Главное внимательность.":
            timur "Ну, делай заметки при расчётах."
            $ timur_relationship += 1
            
        "Легко тебе говорить, ты гений.":
            timur "Просто много практики, ничего особенного."
    
    hide timur

    scene bg classroom

    "Криптография."
    
    $ run_exam("cryptography", resume_music="audio/Soundtracks/hall.mp3")
    
    scene bg hallway
    play music "audio/Soundtracks/hall.mp3" fadein 1.0
    "Первый этап пройден. Ты выходишь, пытаясь расшифровать надпись на автомате с кофе."
    "Надо отойти от крипты."
    
    "Перерыв перед Матаном. Целых 3 часа в аудитории. Будет тяжко."
    
    scene bg hallway
    play music "audio/Soundtracks/hall.mp3" fadein 1.0
    "Преподаватель по анализу пишет на доске формулу на полстены."
    "Кого-то трясет, кто-то прячет шпоры, а кто-то уже смирился."
    
    "Ты собираешь волю в кулак."
    
    $ run_exam("math_analysis", resume_music="audio/Soundtracks/hall.mp3")
    
    scene bg room
    play music "audio/Soundtracks/Room.mp3" fadein 1.0
    "Вечер. Ты лежишь на полу и смотришь в потолок."
    "Самое трудное позади."
    
    "Завтра последний день перед финалом. Нужно собраться."
    
    jump day4

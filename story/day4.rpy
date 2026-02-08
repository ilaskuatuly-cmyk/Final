label day4:
    scene bg room
    
    
    show screen day_indicator("День 4")
    
    "Четверг. Затишье перед бурей."
    "Завтра финал. Английский и Сети."
    
    "Вся группа собралась в столовой."
    
    scene bg cafeteria # Placeholder
    play music "audio/Soundtracks/Cafeteria.mp3" fadein 1.0
    
    show ayan at left
    show diana at right
    show timur at center
    
    diana "Я слышала, на Сетях будет задача про трассировку. Это же ад!"
    ayan "Просто логика, Диана. Если пакет не пришел, значит, он где-то застрял."
    timur "Или его перехватили."
    
    "Все нервничают. От тебя зависит настроение группы."
    
    menu:
        "Поддержать всех! Мы команда!":
            mc "Ребята, мы сдали Матан. Мы сдали Крипту. Сети — это мелочь."
            "Аян улыбается."
            diana "По сути да, должно быть легче."
            timur "Логично."
            $ ayan_relationship += 1
            $ diana_relationship += 1
            $ timur_relationship += 1
            
        "Предложить устроить прогон по билетам.":
            mc "Давайте меньше паники, больше дела. Давайте пройдемся по терминам."
            "Было душно, но это лучше чем ничего."
            # Maybe slight bonus to next exams? Implicitly logic works.
            $ ayan_relationship += 1
            
        "Уйти готовиться самому (Сохранить силы).":
             mc "Я пас. Хочу лечь пораньше."
             "Ты уходишь. Они смотрят тебе вслед."
             # Social isolation path

    hide ayan
    hide diana
    hide timur
    
    scene bg room
    play music "audio/Soundtracks/Room.mp3" fadein 1.0
    "Ты перечитываешь конспекты по английскому."
    "Лишь бы попалась легкая тема."
    "Ладно, пора спать."
    
    jump day5

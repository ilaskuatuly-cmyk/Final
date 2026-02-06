label day4:
    scene bg room
    
    show screen day_indicator("День 4")
    
    "Четверг. Тишина перед бурей."
    "Завтра финал. Английский и Сети."
    
    "Вся группа собирается в столовой для 'последней вечери'."
    
    scene bg cafeteria # Placeholder
    
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
            diana "Ты прав, Алекс. Мы справимся!"
            timur "Логично."
            $ ayan_relationship += 1
            $ diana_relationship += 1
            $ timur_relationship += 1
            
        "Предложить устроить прогон по билетам.":
            mc "Давайте меньше паники, больше дела. Диана, гоняй нас по терминам."
            "Это было жестко, но полезно."
            # Maybe slight bonus to next exams? Implicitly logic works.
            $ ayan_relationship += 1
            
        "Уйти готовиться самому (Сохранить силы).":
             mc "Я пас. Мне нужно выспаться."
             "Ты уходишь. Они смотрят тебе вслед."
             # Social isolation path

    hide ayan
    hide diana
    hide timur
    
    scene bg room
    "Ты перечитываешь конспекты по английскому."
    "Past Perfect Continuous... В чем разница с Past Perfect?"
    "Завтра узнаем."
    
    jump day5

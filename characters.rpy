# Определение персонажей
# Спрайты персонажей (автоматически ищутся в images/, но определяем явно для гибкости)
image ayan = "images/Ayan.png"
image diana = "images/Diana.png"
image timur = "images/Timur.png"
image alina = "images/Alina.png"

# Определение персонажей с привязкой к тегам изображений
define mc = Character("[player_name]", color="#ffffff") # Главный герой
define ayan = Character("Аян", color="#3498db", image="ayan") # Синий - логика, программирование
define diana = Character("Диана", color="#e74c3c", image="diana") # Красный - социальная активность
define timur = Character("Тимур", color="#9b59b6", image="timur") # Фиолетовый - криптография, загадочность
define alina = Character("Алина", color="#2ecc71", image="alina") # Зеленый - рост, языки
define teacher = Character("Преподаватель", color="#f1c40f")

# Общие стили для экзаменов
style exam_text:
    size 30
    color "#000000"
    xalign 0.5
    text_align 0.5

style exam_button_text:
    size 25
    color "#ffffff"
    hover_color "#cccccc"

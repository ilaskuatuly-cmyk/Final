# === GENERIC EXAM SCREENS ===

screen exam_background(title):
    add "#f0f0f0"
    frame:
        xalign 0.5
        yalign 0.05
        padding (20, 20)
        background "#2c3e50"
        hbox:
            spacing 20
            text title size 30 bold True color "#ecf0f1"
            
            # Кнопка пропуска
            textbutton "Пропустить фазу":
                action Return("skip")
                text_size 14
                text_color "#bdc3c7"
                text_hover_color "#fff"
                yalign 0.5

# 1. Error Hunt Screen
# Displays code lines. Returns index of clicked line.
screen exam_click_error_screen(title, code_lines):
    use exam_background(title)
    
    vbox:
        xalign 0.5
        yalign 0.4
        spacing 10
        text "Нажмите на строку с ошибкой:" color "#000" size 24
        
        for i, line in enumerate(code_lines):
            button:
                style "exam_button"
                xsize 800
                action Return(i)
                text line font "DejaVuSans.ttf" style "exam_button_text" xalign 0.0 substitute False

# 2. Input Screen
# Text prompt and input field.
screen exam_input_screen(title, prompt):
    use exam_background(title)
    
    default user_input = ""
    
    vbox:
        xalign 0.5
        yalign 0.4
        spacing 20
        
        frame:
            padding (20, 20)
            text prompt color "#000" font "DejaVuSans.ttf" substitute False
            
        input:
            value ScreenVariableInputValue("user_input")
            length 10
            allow "0123456789"
            color "#000"
            size 40
            
        textbutton "Подтвердить":
            style "exam_button"
            text_style "exam_button_text"
            action Return(user_input)

# 3. Ordering Screen
# Clicking logic to order items.
screen exam_ordering_screen(title, items):
    default selected_indices = []
    
    use exam_background(title)
    
    vbox:
        xalign 0.5
        yalign 0.2
        spacing 10
        text "Нажмите на элементы в правильном порядке:" color "#000" size 24
        
        # Result Preview
        frame:
            xsize 900
            ysize 250
            background "#ecf0f1"
            vbox:
                spacing 5
                for idx in selected_indices:
                    text items[idx] color "#2980b9" font "DejaVuSans.ttf" size 22 substitute False
        
        # Available Items
        vbox:
            spacing 5
            for i, item in enumerate(items):
                if i not in selected_indices:
                    button:
                        style "exam_button"
                        xsize 900
                        action SetScreenVariable("selected_indices", selected_indices + [i])
                        text item font "DejaVuSans.ttf" style "exam_button_text" xalign 0.0 substitute False

        textbutton "Готово":
            style "exam_button"
            text_style "exam_button_text"
            yalign 1.0
            xalign 0.5
            action Return(selected_indices)
            
        textbutton "Сброс":
            style "exam_button"
            text_style "exam_button_text"
            yalign 1.0
            xalign 0.8
            action SetScreenVariable("selected_indices", [])

# 4. Multi-select Screen
# Toggle tags.
screen exam_multiselect_screen(title, prompt, options):
    default selected = set()
    
    use exam_background(title)
    
    vbox:
        xalign 0.5
        yalign 0.2
        spacing 20
        
        text prompt color "#000" size 28 italic True xalign 0.5 text_align 0.5 xsize 1000
        
        grid 2 3: # Assuming max 6 options
            xalign 0.5
            spacing 15
            for opt in options:
                button:
                    style "exam_button"
                    xsize 400
                    action ToggleSetMembership(selected, opt)
                    background ("#27ae60" if opt in selected else "#34495e")
                    text opt style "exam_button_text"

        textbutton "Подтвердить выбор":
            style "exam_button"
            text_style "exam_button_text"
            xalign 0.5
            action Return(selected)

# 5. Simple Choice Screen
screen exam_choice_screen(title, question, options):
    use exam_background(title)
    
    vbox:
        xalign 0.5
        yalign 0.3
        spacing 20
        
        text question color "#000" size 28 xalign 0.5
        
        for i, opt in enumerate(options):
            button:
                style "exam_button"
                xsize 800
                action Return(i)
                text opt style "exam_button_text"

# Global Styles
style exam_button:
    padding (15, 15)
    background "#34495e"
    hover_background "#2c3e50"

    size 22
    color "#ffffff"
    xalign 0.5
    text_align 0.5

# 6. Adjuster Screen (Slider/Counter)
# Used for Caesar Cipher and Math Limits
screen exam_adjuster_screen(title, prompt, initial_value, min_val, max_val):
    default current_val = initial_value
    
    use exam_background(title)
    
    vbox:
        xalign 0.5
        yalign 0.3
        spacing 30
        
        text prompt color "#000" size 30 xalign 0.5
        
        hbox:
            spacing 20
            xalign 0.5
            textbutton "-":
                action SetScreenVariable("current_val", max(min_val, current_val - 1))
                style "exam_button"
                text_style "exam_button_text"
                
            text "[current_val]" size 50 color "#000" yalign 0.5
            
            textbutton "+":
                action SetScreenVariable("current_val", min(max_val, current_val + 1))
                style "exam_button"
                text_style "exam_button_text"

        textbutton "Подтвердить":
            action Return(current_val)
            xalign 0.5
            style "exam_button"
            text_style "exam_button_text"

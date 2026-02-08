init python:
    # Словарь для хранения оценок (предмет -> баллы 0-100)
    exam_grades = {
        "programming": 0,
        "psychology": 0,
        "cryptography": 0,
        "math_analysis": 0,
        "english": 0,
        "networks": 0
    }

    # Флаги отношений
    ayan_relationship = 0
    diana_relationship = 0
    timur_relationship = 0
    alina_relationship = 0
    
    # Minigame vars
    current_lockpicks = 0

    # Сюжетные флаги
    helped_ayan = False 
    trusted_diana = False 
    bonded_timur = False 
    practiced_alina = False
    
    player_name = "Студент"

    def normalize_score(value):
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, (list, tuple)):
            for item in reversed(value):
                if isinstance(item, (int, float)):
                    return item
            return 0
        try:
            return int(value)
        except Exception:
            return 0

    def get_letter_grade(score):
        score = normalize_score(score)
        if score >= 95: return "A"
        if score >= 90: return "A-"
        if score >= 85: return "B+"
        if score >= 80: return "B"
        if score >= 75: return "B-"
        if score >= 70: return "C+"
        if score >= 65: return "C"
        if score >= 60: return "C-"
        return "F"

    def get_gpa_point(score):
        score = normalize_score(score)
        if score >= 95: return 4.0
        if score >= 90: return 3.67
        if score >= 85: return 3.33
        if score >= 80: return 3.0
        if score >= 75: return 2.67
        if score >= 70: return 2.33
        if score >= 65: return 2.0
        if score >= 60: return 1.67
        return 0.0

    def calculate_gpa():
        total_gpa = 0
        count = 0
        for subject, grade in exam_grades.items():
            total_gpa += get_gpa_point(grade)
            count += 1
        if count == 0:
            return 0.0
        return round(total_gpa / count, 2)

default student_name = "Алекс"

default studied_matan = False


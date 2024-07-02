import random
from decimal import Decimal

from django.db.models import Sum


def calculate_life_expectancy(user_quiz) -> dict:
    weight = int(user_quiz.weight)
    height = int(user_quiz.height)
    location = user_quiz.location
    user_answers = user_quiz.user_answers.all()
    questions = user_answers.values_list('question', flat=True).distinct()

    answers_duration = user_answers.aggregate(total=Sum('answers__duration')).get('total', 0)
    answers_duration = answers_duration if answers_duration else 0
    location_duration = location.duration if location else 0
    bmi_duration = _calculate_bmi_duration(weight, height) if weight and height else 0
    duration = answers_duration + bmi_duration + location_duration

    y = _generate_random_number(5.0, 15.0, 0.1)
    accuracy = ((len(questions) + 2) / 27) * 100 - 12.7 - y
    if accuracy < 20:
        accuracy = 20
    return {
        'duration': round(duration, 2),
        'accuracy': round(accuracy, 2)
    }


def _calculate_bmi_duration(weight: int, height: int) -> float:
    height /= 100
    BMI = weight / (height * height)
    BMI = round(BMI, 2)
    if BMI < 25:
        BMI_duration = 0
    elif 25 <= BMI < 30:
        BMI_duration = -2.4
    elif 30 <= BMI < 35:
        BMI_duration = -5.9
    elif 35 <= BMI < 40:
        BMI_duration = -7.8
    else:
        BMI_duration = -9.5

    return BMI_duration


def _generate_random_number(start: float, end: float, step: float) -> float:
    start = Decimal(start)
    end = Decimal(end)
    step = Decimal(step)
    steps = int((end - start) / step)
    random_step = random.randint(0, steps)
    random_number = start + random_step * step
    return float(random_number)

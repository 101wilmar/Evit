import io
import random
from decimal import Decimal
from urllib.parse import quote

import pdfkit
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template

from constants import PATH_WKHTMLTOPDF


def get_user_quiz_pdf(user_quiz, return_io: bool = False):
    user: User = user_quiz.user
    user_quizzes_ids = list(user.user_quizzes.all().order_by('created_at').values_list('id', flat=True))
    count = user_quizzes_ids.index(user_quiz.id)
    template = get_template('app/user_quiz/recommendation/pdf.html')
    recommendation_user_answers = user_quiz.user_answers.annotate(
        duration_sum=Sum('answers__duration')
    ).exclude(
        question__is_recommendation=False
    ).filter(
        duration_sum__lt=0,
    ).order_by('question_id')
    recommendation_user_answers = recommendation_user_answers.select_related('question')
    html = template.render({
        'user': user,
        'user_quiz': user_quiz,
        'recommendation_user_answers': recommendation_user_answers
    })
    options = {
        'margin-top': '0.3cm',
        'margin-right': '1.0cm',
        'margin-bottom': '0.0cm',
        'margin-left': '2.0cm',
        'page-size': 'A4',
        'copies': 1,
        # 'dpi': 96
    }

    config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF) if PATH_WKHTMLTOPDF else None

    pdf = pdfkit.from_string(html, False, options, configuration=config)
    if return_io:
        return io.BytesIO(pdf)
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"No_{count}_Recommendation_E-VIT_{user_quiz.created_at.strftime('%d-%m-%Y')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{quote(filename)}"'
    return response


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


#def _calculate_bmi_duration(weight: int, height: int) -> float:
#    height /= 100
#    BMI = weight / (height * height)
#    BMI = round(BMI, 2)
#    if BMI < 25:
#        BMI_duration = 0
#    elif 25 <= BMI < 30:
#        BMI_duration = -2.4
#    elif 30 <= BMI < 35:
#        BMI_duration = -5.9
#    elif 35 <= BMI < 40:
#        BMI_duration = -7.8
#    else:
#        BMI_duration = -9.5

#    return BMI_duration
def _calculate_bmi_duration(weight: int, height: int) -> Decimal:
    height = Decimal(height) / Decimal(100)
    BMI = Decimal(weight) / (height * height)
    BMI = round(BMI, 2)
    if BMI < 25:
        BMI_duration = Decimal(0)
    elif 25 <= BMI < 30:
        BMI_duration = Decimal(-2.4)
    elif 30 <= BMI < 35:
        BMI_duration = Decimal(-5.9)
    elif 35 <= BMI < 40:
        BMI_duration = Decimal(-7.8)
    else:
        BMI_duration = Decimal(-9.5)

    return BMI_duration

def _generate_random_number(start: float, end: float, step: float) -> float:
    start = Decimal(start)
    end = Decimal(end)
    step = Decimal(step)
    steps = int((end - start) / step)
    random_step = random.randint(0, steps)
    random_number = start + random_step * step
    return float(random_number)

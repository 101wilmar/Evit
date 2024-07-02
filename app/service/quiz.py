import random
from decimal import Decimal

from django.db.models import Sum

from app.models import Question, Answer, UserAnswer, Location
from app.service.user_quiz import calculate_life_expectancy


def save_user_quiz(user_quiz, data):
    full_name = data.get('full_name')
    current_age = data.get('current_age')
    height = data.get('height')
    weight = data.get('weight')
    location_id = data.get('location')

    user_quiz.full_name = full_name
    user_quiz.current_age = current_age
    user_quiz.height = height
    user_quiz.weight = weight
    if location_id:
        try:
            location_id = int(location_id)
            location = Location.objects.get(id=location_id)
            user_quiz.location = location
        except:
            ...

    for question_index in data:
        try:
            int(question_index)
            answer_indexes = data.getlist(question_index, [])
            if len(answer_indexes) <= 1 and answer_indexes[0] == '':
                continue
            question = Question.objects.get(pk=question_index)

            answers = []
            for answer_index in answer_indexes:
                answer_index = int(answer_index)
                answer = Answer.objects.get(pk=answer_index)
                answers.append(answer)

            user_answer = UserAnswer.objects.get_or_create(
                user_quiz=user_quiz,
                question=question
            )
            if user_answer[1]:
                user_answer[0].save()
            user_answer = user_answer[0]

            user_answer.answers.add(*answers)
            user_answer.save()
        except:
            continue
    user_quiz.save()


def set_life_expectancy(user_quiz):
    duration_and_accuracy = calculate_life_expectancy(user_quiz)
    duration = duration_and_accuracy.get('duration', 0)
    accuracy = duration_and_accuracy.get('accuracy', 0)
    user_quiz.duration = duration
    user_quiz.accuracy = accuracy
    user_quiz.save()


def get_difference(last_quiz, previous_quiz):
    previous_questions = previous_quiz.user_answers.annotate(duration_sum=Sum('answers__duration'))
    last_questions = last_quiz.user_answers.annotate(duration_sum=Sum('answers__duration'))

    previous_dict = {}
    last_dict = {}

    for i in previous_questions:
        previous_dict[i.question.id] = {
            'text': i.question.text,
            'duration': i.duration_sum,
        }
    for i in last_questions:
        last_dict[i.question.id] = {
            'duration': i.duration_sum,
        }

    improved_results = {}
    worsening_results = {}
    for i in previous_dict:
        previous_result = previous_dict.get(i, {}).get('duration')
        last_result = last_dict.get(i, {}).get('duration')
        if not last_result:
            continue
        if previous_result < last_result:
            improved_results[i] = {
                'text': previous_dict.get(i).get('text'),
                'difference': round(last_result - previous_result, 2),
            }
        elif last_result < previous_result:
            worsening_results[i] = {
                'text': previous_dict.get(i).get('text'),
                'difference': round(previous_result - last_result, 2),
            }
    return improved_results, worsening_results

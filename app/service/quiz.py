import random
from decimal import Decimal

from django.db.models import Sum

from app.models import Question, Answer, UserAnswer, Location


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



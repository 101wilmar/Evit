from django.contrib.auth.models import User
from django.db import models

from app.models import BaseModel, Question
from .location import Location
from .quiz import Quiz, Answer
from ..service.user_quiz import calculate_life_expectancy


class UserQuiz(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_quizzes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_quizzes')

    full_name = models.CharField(max_length=120)
    email = models.EmailField(null=True, blank=True)
    current_age = models.IntegerField(default=0, null=True, blank=True)
    weight = models.IntegerField(default=0, null=True, blank=True)
    height = models.IntegerField(default=0, null=True, blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_quizzes'
    )

    accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Точность')
    duration = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Продолжительность')

    class Meta:
        verbose_name = 'Тест пользователя'
        verbose_name_plural = 'Тесты пользователя'

    def __str__(self):
        return self.user.username

    @property
    def get_life_expectancy_and_accuracy(self):
        data = calculate_life_expectancy(self)
        return data


class UserAnswer(BaseModel):
    user_quiz = models.ForeignKey(
        UserQuiz, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_answers'
    )
    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_answers'
    )
    answers = models.ManyToManyField(Answer)

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователя'
        unique_together = [
            ['user_quiz', 'question'],
        ]

    def __str__(self):
        return f'{self.user_quiz.user.username}'

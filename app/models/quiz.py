from django.db import models

from app.models.base import BaseModel


class Quiz(BaseModel):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Опросник'
        verbose_name_plural = 'Опросники'

    def __str__(self):
        return self.name


class Question(BaseModel):
    class DisplayTypeChoices(models.TextChoices):
        SELECT = 'select', 'Выпадающий список'
        SWITCH = 'switch', 'Переключатель'

    text = models.TextField(verbose_name='Текст')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    is_required = models.BooleanField(default=False, verbose_name='Обязательное поле')
    is_multiple = models.BooleanField(default=False, verbose_name='Несколько вариантов')
    is_recommendation = models.BooleanField(default=False, verbose_name='Есть ли рекомендация')

    recommendation = models.TextField(null=True, blank=True, verbose_name='Рекомендация')
    display_type = models.CharField(
        max_length=128, choices=DisplayTypeChoices.choices, default=DisplayTypeChoices.SELECT,
        verbose_name='Как показать'
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'Вопрос №{self.id}'


class Answer(BaseModel):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    duration = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'

    def __str__(self):
        return f'"{self.question.text}" вариант №{self.id}'

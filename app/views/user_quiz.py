from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, get_object_or_404

from app.models import UserQuiz, Location, Answer
from app.models.quiz import Quiz
from app.service.quiz import save_user_quiz
from app.service.user_quiz import calculate_life_expectancy


@login_required
def quiz_list(request):
    user = request.user
    user_quizzes = user.user_quizzes.all().order_by('-created_at')
    return render(request, 'app/user_quiz/list.html', {
        'user_quizzes': user_quizzes
    })


@login_required
def start_quiz(request):
    quiz = Quiz.objects.first()
    questions = quiz.questions.all()
    locations = Location.objects.all().order_by('name')
    return render(request, 'app/quiz/quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'locations': locations
    })


@login_required
def save_quiz(request):
    if request.method != 'POST':
        return redirect(reverse('app:quiz_list'))
    user = request.user
    quiz = Quiz.objects.first()
    user_quiz = UserQuiz.objects.create(
        user=user,
        quiz=quiz
    )
    user_quiz.save()
    data = request.POST
    save_user_quiz(user_quiz, data)
    return redirect(reverse('app:quiz_list'))


@login_required
def quiz_detail(request, user_quiz_id):
    user_quiz = get_object_or_404(UserQuiz, pk=user_quiz_id)
    user_questions_and_answers = {}
    user_answers = user_quiz.user_answers.all()
    answer_ids = user_answers.values_list('answers__id', flat=True)
    user_questions = user_answers.values_list('question_id', flat=True)

    for q in user_questions:
        user_questions_and_answers[q] = user_answers.filter(question_id=q).values_list('answers__text', flat=True)
        # user_questions_and_answers[q] = Answer.objects.filter(question_id=q, id__in=answer_ids)

    quiz = user_quiz.quiz
    quiz_questions = quiz.questions.all()

    data = calculate_life_expectancy(user_quiz)
    return render(request, 'app/user_quiz/detail.html', {
        'user_quiz': user_quiz,
        'user_questions_and_answers': user_questions_and_answers,
        'quiz_questions': quiz_questions,
        'data': data
    })
